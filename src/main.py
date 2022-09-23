import json
import logging
import os
import re
import shlex
from datetime import datetime

import firebase_admin
import google.oauth2.id_token
import requests
from discord import DMChannel, Embed, Intents
from discord.abc import GuildChannel
from discord.ext.commands import Bot, Context
from discord.member import Member as member_type
from discord.message import Message as message_type
from dotenv import load_dotenv
from firebase_admin import credentials, firestore
from google.auth.transport.requests import Request
from google.cloud.firestore_v1.base_document import DocumentSnapshot
from google.cloud.firestore_v1.collection import CollectionReference
from google.cloud.firestore_v1.document import DocumentReference
from google.cloud.pubsub_v1 import PublisherClient
from google.cloud.pubsub_v1.publisher.futures import Future
from requests import Response

load_dotenv()

LOGGER: logging.Logger = logging.getLogger(__name__)
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
FUNCTION_BASE_RUL = "https://us-central1-archy-f06ed.cloudfunctions.net/"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Discord bot settings
intents = Intents.all()

bot: Bot = Bot(command_prefix="!", description="Serverless commands discord bot", intents=intents)

# Gcloud auth settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"
request = Request()

# Firestore
PROJECT_ID = "archy-f06ed"

cred = credentials.Certificate("./key.json")
firebase_admin.initialize_app(cred)
db = firestore.client()


def is_active_command(server_id: str, command_name: str) -> bool:
    """Check if a command is active in the firestore db."""
    function_collection: CollectionReference = db.collection("servers").document(server_id).collection("functions")
    doc_ref: DocumentReference = function_collection.document(command_name)
    doc: DocumentSnapshot = doc_ref.get()

    if doc.exists:
        return doc.get("active")

    return False


def create_user(member: member_type) -> bool:
    """Create a user in the firestore db."""
    server_id = str(member.guild.id)
    user_collection: CollectionReference = db.collection("servers").document(server_id).collection("users")
    doc_ref: DocumentReference = user_collection.document(str(member.id))
    doc: DocumentSnapshot = doc_ref.get()

    # If user doesn't exist, create it with user_id as the document id
    if not doc.exists:
        doc_ref.set(
            {
                "total_exp": 0,
                "exp_toward_next_level": 0,
                "level": 0,
                "message_count": 0,
                "last_message_timestamp": datetime.now().strftime(DATETIME_FORMAT),
                "username": str(member.name),
                "avatar_url": str(member.avatar.url),
            }
        )

        return True

    # If user exists, return False
    return False


def update_user_role(server_id: str, user_id: str):
    """Publish message to the update_user_role topic."""
    topic_id = "update_user_role"

    publisher = PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)

    data = {"server_id": server_id, "user_id": user_id}

    encoded_data: bytes = json.dumps(data, indent=2).encode("utf-8")
    future: Future = publisher.publish(topic_path, encoded_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")


def send_message_to_channel(channel_id: str, message: str):
    """Publish message to the channel_message_discord topic."""
    topic_id = "channel_message_discord"

    publisher = PublisherClient()
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)
    data = {"channel_id": channel_id, "message": message}

    user_encode_data: bytes = json.dumps(data, indent=2).encode("utf-8")
    future: Future = publisher.publish(topic_path, user_encode_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")


def send_welcome_message(channel_id: str, username: str, avatar_url):
    publisher = PublisherClient()
    topic_path = publisher.topic_path("archy-f06ed", "generate_welcome_image")

    payload = {"username": username, "avatar_url": avatar_url}

    data = {"channel_id": channel_id, "payload": payload}

    user_encode_data = json.dumps(data, indent=2).encode("utf-8")
    future: Future = publisher.publish(topic_path, user_encode_data)

    print(f"Message id: {future.result()}")
    print(f"Published message to {topic_path}.")


@bot.event
async def on_member_join(member: member_type) -> None:
    LOGGER.warning("Member %s has just joined the server %s", member.name, member.guild.name)

    server_id = str(member.guild.id)

    channel_collection: CollectionReference = db.collection("servers").document(server_id).collection("channels")
    doc_ref: DocumentReference = channel_collection.document("welcome")
    doc: DocumentSnapshot = doc_ref.get()

    if doc.exists:
        channel: GuildChannel = member.guild.get_channel(int(doc.get("channel_id")))

        if channel is None:
            LOGGER.warning(
                "Channel id %s doesn't exist anymore or is invalid for document welcome for server %s",
                str(doc.get("channel_id")),
                str(member.guild.name),
            )
        else:
            send_welcome_message(str(channel.id), str(member.name), str(member.avatar.url))

    # Create user in firestore db if doesn't exist
    is_new_user = create_user(member)

    update_user_role(server_id, str(member.id))

    print(f"User created: {is_new_user}")


@bot.event
async def on_message(message: message_type) -> None:
    LOGGER.warning("Message from %s is: %s", message.author, message.content)

    if (
        isinstance(message.channel, DMChannel)
        and message.author != bot.user
        and message.content == os.environ["UQAM_PASSPHRASE"]
    ):
        await message.channel.send(f"`{os.environ['UQAM_FLAG']}`")
        return

    ctx: Context = await bot.get_context(message)
    if ctx.invoked_with:
        if not is_active_command(str(ctx.guild.id), str(ctx.invoked_with)):
            await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
            return

        function_path = f"{FUNCTION_BASE_RUL}{ctx.invoked_with}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "server_id": str(ctx.guild.id),
                    "server_name": str(ctx.message.guild.name),
                    "user_id": str(ctx.author.id),
                    "username": str(ctx.author.name),
                    "channel_id": str(message.channel.id),
                    "message_id": str(message.id),
                    "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
                    "params": shlex.split(message.content)[1:],
                }
            ),
        )

        if response.status_code == 200 and response.content:
            if re.search("https://*", response.content.decode("utf-8")):
                await ctx.send(response.content.decode("utf-8"))
            else:
                embed: Embed = Embed(
                    description=response.content.decode("utf-8"),
                    color=0x04AA6D,
                )
                await ctx.send(embed=embed)

    # Add exp to the user for every message send
    elif not message.author.bot:

        publisher = PublisherClient()
        topic_path = publisher.topic_path("archy-f06ed", "exp_discord")

        data = {
            "server_id": str(ctx.guild.id),
            "user_id": str(ctx.author.id),
            "server_name": str(ctx.message.guild.name),
            "username": str(ctx.author.name),
            "avatar_url": f"{ctx.author.avatar.url}",
        }

        user_encode_data = json.dumps(data, indent=2).encode("utf-8")
        future: Future = publisher.publish(topic_path, user_encode_data)

        print(f"Message id: {future.result()}")
        print(f"Published message to {topic_path}.")

    if message.content == f"<@{bot.user.id}>":
        await ctx.send("> Who Dares Summon Me?")


@bot.event
async def on_message_edit(before: message_type, after: message_type) -> None:
    LOGGER.warning(before)
    LOGGER.warning(after)


bot.remove_command("help")
bot.run(DISCORD_API_TOKEN)
