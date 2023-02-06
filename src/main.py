import base64
import json
import logging
import os
import re
from datetime import datetime
from io import BytesIO
from typing import Dict

import firebase_admin
import google.oauth2.id_token
import requests
from discord import DMChannel, Embed, File, Guild, Intents, Option, User
from discord.abc import GuildChannel
from discord.ext.commands import Bot, Context
from discord.member import Member as member_type
from discord.message import Message as message_type
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from google.auth.transport.requests import Request
from google.cloud.firestore import Increment
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.pubsub_v1 import PublisherClient
from requests import Response

load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT")

LOGGER: logging.Logger = logging.getLogger(__name__)
FUNCTION_BASE_URL = "https://us-central1-archy-f06ed.cloudfunctions.net/"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
DISCORD_API_TOKEN = os.getenv(f"DISCORD_API_TOKEN_{ENVIRONMENT.upper()}")
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX")

# Discord bot settings
intents = Intents.all()

bot: Bot = Bot(
    command_prefix=COMMAND_PREFIX,
    description="Serverless commands discord bot",
    intents=intents,
)

# Firestore
PROJECT_ID = "archy-f06ed"
KEY_FILE = "./key.json"


# Gcloud auth settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = KEY_FILE
request = Request()


@bot.event
async def on_guild_join(guild: Guild) -> None:

    data = {
        "server_name": str(guild.name),
        "server_id": str(guild.id),
        "server_icon": f"{guild.icon_url.BASE}{guild.icon_url._url}",  # pylint: disable=protected-access
        "member_count": int(guild.member_count),
    }

    server_list_collection: CollectionReference = db.collection("serverList")
    server_ref = server_list_collection.document(data["server_id"])
    doc = server_ref.get()

    if not doc.exists:
        server_ref.set(data)
    else:
        server_ref.update({"member_count": data["member_count"]})


def is_active_command(server_id: str, command_name: str) -> bool:
    """Check if a command is active in the firestore db."""
    if (command_name.startswith(("dev_", "team_"))) and server_id == "964701887540645908":
        return True

    function_collection: CollectionReference = db.collection("servers").document(server_id).collection("functions")
    doc_ref: DocumentReference = function_collection.document(command_name)
    doc: DocumentSnapshot = doc_ref.get()

    return doc.get("active") if doc.exists else False


def create_user(member: member_type) -> None:
    """Create a user in the firestore db if he doesn't exist already."""
    server_id = str(member.guild.id)
    user_collection: CollectionReference = db.collection("servers").document(server_id).collection("users")
    doc_ref: DocumentReference = user_collection.document(str(member.id))
    doc: DocumentSnapshot = doc_ref.get()

    if not doc.exists:
        doc_ref.set(
            {
                "total_exp": 0,
                "exp_toward_next_level": 0,
                "level": 0,
                "message_count": 0,
                "last_message_timestamp": datetime.now().strftime(DATETIME_FORMAT),
                "username": str(member.name),
                "avatar_url": str(member.avatar.url) if member.avatar else None,
            }
        )

        db.collection("serverList").document(server_id).update({"member_count": Increment(1)})


def update_user_role(server_id: str, user_id: str) -> None:
    """Publish message to the update_user_role topic."""
    topic_id = "update_user_role"
    data = {"server_id": server_id, "user_id": user_id}
    publish_message(data, topic_id)


def send_message_to_channel(channel_id: str, message: str) -> None:
    """Publish message to the channel_message_discord topic."""
    topic_id = "channel_message_discord"
    data = {"channel_id": channel_id, "message": message}
    publish_message(data, topic_id)


def send_welcome_message(channel_id: str, username: str, avatar_url: str) -> None:
    """Publish message to generate_welcome_image."""
    topic_id = "generate_welcome_image"
    payload = {"username": username, "avatar_url": avatar_url}
    data = {"channel_id": channel_id, "payload": payload}
    publish_message(data, topic_id)


def publish_message(data: Dict[str, str], topic_id: str) -> None:
    """Publish message to the selected topic."""

    publisher = PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, f"{ENVIRONMENT}_{topic_id}")

    user_encode_data: bytes = json.dumps(data, indent=2).encode("utf-8")
    publisher.publish(topic_path, user_encode_data)


def increment_command_count(server_id: str, command_name: str) -> None:
    function_collection: CollectionReference = db.collection("servers").document(server_id).collection("functions")
    doc_ref: DocumentReference = function_collection.document(command_name)
    if doc_ref.get().exists:
        doc_ref.update({"count": Increment(1)})


@bot.event
async def on_member_join(member: member_type) -> None:
    LOGGER.warning("Member %s has just joined the server %s", member.name, member.guild.name)

    server_id = str(member.guild.id)

    channel_collection: CollectionReference = db.collection("servers").document(server_id).collection("channels")
    doc_ref: DocumentReference = channel_collection.document("welcome")
    doc: DocumentSnapshot = doc_ref.get()

    if doc.exists:
        channel: GuildChannel = member.guild.get_channel(int(doc.get("channel_id")))

        if channel:
            send_welcome_message(str(channel.id), str(member.name), str(member.avatar.url))

    create_user(member)

    update_user_role(server_id, str(member.id))


@bot.event
async def on_member_remove(member: member_type) -> None:
    server_id = str(member.guild.id)
    db.collection("serverList").document(server_id).update({"member_count": Increment(-1)})


@bot.event
async def on_message(message: message_type) -> None:
    if message.author.bot:
        return

    LOGGER.warning("Message from %s is: %s", message.author, message.content)

    if isinstance(message.channel, DMChannel):
        if message.content == os.environ["UQAM_PASSPHRASE"]:
            await message.channel.send(f"`{os.environ['UQAM_FLAG']}`")
        return

    ctx: Context = await bot.get_context(message)

    server_id = str(ctx.guild.id)

    data = {
        "server_id": server_id,
        "server_name": str(ctx.message.guild.name),
        "user_id": str(ctx.author.id),
        "username": str(ctx.author.name),
        "environment": ENVIRONMENT,
    }
    if ctx.invoked_with and not ctx.author.bot:
        command_name = str(ctx.invoked_with)

        data["channel_id"] = str(message.channel.id)
        data["channel_name"] = str(message.channel.name)
        data["message_id"] = str(message.id)
        data["mentions"] = [str(user_id) for user_id in ctx.message.raw_mentions]
        data["params"] = message.content.split()[1:]

        response = await treat_command(ctx, command_name, data)

        if re.search("https://*", response):
            await ctx.send(response)
        elif re.search("data:image/png;base64,*", response):
            await ctx.send(file=File(BytesIO(base64.b64decode(response.split(",")[1])), "image.png"))
        else:
            embed: Embed = Embed(
                description=response,
                color=0x04AA6D,
            )
            await ctx.send(embed=embed)

    elif not message.author.bot:

        if ctx.author.avatar:
            data["avatar_url"] = ctx.author.avatar.url

        publish_message(data, "exp_discord")

    if message.content == f"<@{bot.user.id}>":
        await ctx.send("> Who Dares Summon Me?")


async def treat_command(_ctx: Context, command_name: str, data: Dict) -> None:
    data["environment"] = ENVIRONMENT

    if not is_active_command(data["server_id"], command_name):
        return "https://cdn.discordapp.com/emojis/823403768448155648.webp"

    function_path = get_function_path(command_name)

    google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

    response: Response = requests.post(
        function_path,
        headers={
            "Authorization": f"Bearer {google_auth_token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )
    increment_command_count(data["server_id"], command_name)

    if response.status_code == 200 and response.content:
        return response.content.decode("utf-8")


def get_function_path(command_name: str) -> str:
    if command_name.startswith(("dev_", "team_")):
        return f"{FUNCTION_BASE_URL}{command_name}"
    return f"{FUNCTION_BASE_URL}{ENVIRONMENT}_{command_name}"


@bot.slash_command(description="go")
async def go(ctx: Context) -> None:  # pylint: disable=invalid-name

    server_id = str(ctx.guild.id)
    command_name = "go"

    data = {
        "server_id": server_id,
        "channel_id": "Slash_Command",
    }
    interaction = await ctx.respond("Loading...")
    message = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(content=message)


@bot.slash_command(description="Hello! :)")
async def hello(ctx: Context) -> None:

    command_name = "hello"

    data = {
        "server_id": str(ctx.guild.id),
        "user_id": str(ctx.author.id),
    }
    interaction = await ctx.respond("Loading...")
    message = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(content=message)


@bot.slash_command(description="Return the leaderboard")
async def leaderboard(ctx: Context) -> None:

    command_name = "leaderboard"

    data = {
        "server_id": str(ctx.guild.id),
    }

    interaction = await ctx.respond("Loading...")
    message = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(content=message)


@bot.slash_command(description="answers your question")
async def answer(ctx: Context, question: Option(str, "your question", required=True)) -> None:

    command_name = "answer"

    data = {
        "server_id": str(ctx.guild.id),
    }

    interaction = await ctx.respond("Loading...")
    response = f"Question: {question}\nAnswer: {await treat_command(ctx, command_name, data)}"

    await interaction.edit_original_response(content=response)


@bot.slash_command(description="Request a gif")
async def gif(ctx: Context, query: Option(str, "query to search", required=True)) -> None:

    command_name = "gif"

    data = {
        "server_id": str(ctx.guild.id),
        "params": str(query.split(" ")),
    }

    interaction = await ctx.respond("Loading...")
    message = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(content=message)


@bot.slash_command(description="Template function in Java")
async def java(ctx: Context) -> None:

    command_name = "java"

    data = {
        "server_id": str(ctx.guild.id),
    }

    interaction = await ctx.respond("Loading...")
    message = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(content=message)


@bot.slash_command(description="Return a random froge")
async def froge(ctx: Context) -> None:

    command_name = "froge"

    data = {
        "server_id": str(ctx.guild.id),
    }

    interaction = await ctx.respond("Loading...")
    message = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(content=message)


@bot.slash_command(description="Show your level")
async def level(ctx: Context, mention: Option(User, "wanna check someone else's?", required=False)) -> None:

    server_id = str(ctx.guild.id)
    command_name = "level"

    data = {
        "server_id": server_id,
        "server_name": str(ctx.guild.name),
        "user_id": str(ctx.author.id),
    }
    if mention:
        data["mentions"] = [str(mention.id)]

    interaction = await ctx.respond("Loading...")
    response = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(
        content=None,
        file=File(BytesIO(base64.b64decode(response.split(",")[1])), "image.png"),
    )


@bot.slash_command(description="You give me a HTTP code, I give you something nice in return")
async def http(ctx: Context, query: Option(int, "HTTP code", required=True)) -> None:

    command_name = "http"

    data = {
        "server_id": str(ctx.guild.id),
        "params": str(query.split(" ")),
    }

    interaction = await ctx.respond("Loading...")
    message = await treat_command(ctx, command_name, data)
    await interaction.edit_original_response(content=message)


if __name__ == "__main__":

    cred = credentials.Certificate(KEY_FILE)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    bot.remove_command("help")
    bot.run(DISCORD_API_TOKEN)
