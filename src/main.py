import json
import logging
import os
import re
from datetime import datetime
from typing import Dict

import firebase_admin
import google.oauth2.id_token
import requests
from discord import DMChannel, Embed, Guild, Intents, Option, User
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
KEY_FILE = "./key.json"


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
    topic_path = publisher.topic_path(PROJECT_ID, topic_id)

    user_encode_data: bytes = json.dumps(data, indent=2).encode("utf-8")
    publisher.publish(topic_path, user_encode_data)


def increment_command_count(server_id: str, command_name: str) -> None:
    function_collection: CollectionReference = db.collection("servers").document(server_id).collection("functions")
    doc_ref: DocumentReference = function_collection.document(command_name)
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
    }
    if ctx.invoked_with and not ctx.author.bot:
        command_name = str(ctx.invoked_with)

        if not is_active_command(server_id, command_name):
            await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
            return

        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data["channel_id"] = str(message.channel.id)
        data["message_id"] = str(message.id)
        data["mentions"] = [str(user_id) for user_id in ctx.message.raw_mentions]
        data["params"] = message.content.split()[1:]

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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

        increment_command_count(server_id, command_name)

    elif not message.author.bot:

        if ctx.author.avatar:
            data["avatar_url"] = ctx.author.avatar.url

        publish_message(data, "exp_discord")

    if message.content == f"<@{bot.user.id}>":
        await ctx.send("> Who Dares Summon Me?")


@bot.SlashCommand.slash_command(description="answers your question")
async def answer(ctx: Context, question: str) -> None:

    server_id = str(ctx.guild.id)
    command_name = "answer"

    data = {
        "server_id": server_id,
        "server_name": str(ctx.message.guild.name),
        "user_id": str(ctx.author.id),
        "username": str(ctx.author.name),
    }
    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data["channel_id"] = str(ctx.channel.id)
        data["message_id"] = str(ctx.message.id)
        data["mentions"] = [str(user_id) for user_id in ctx.message.raw_mentions]
        data["params"] = [question]

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="ban a user")
async def ban(ctx: Context, user: Option(User, "user to ban", required=True)) -> None:

    server_id = str(ctx.guild.id)
    command_name = "ban"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user.id)],
            "params": [str(user.id)],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="describe a user")
async def describe(ctx: Context, user: Option(User, "user to describe", required=False)) -> None:

    server_id = str(ctx.guild.id)
    command_name = "kick"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user.id)],
            "params": [str(user.id)],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="request a froge")
async def froge(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "froge"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="request a gif")
async def gif(ctx: Context, query: Option(str, "query to search", required=False)) -> None:

    server_id = str(ctx.guild.id)
    command_name = "gif"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [query.split(" ")],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="go")
async def go_(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "go"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="hello! :)")
async def hello(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "hello"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="Get help about the bot")
async def help_(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "help"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="java")
async def java(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "java"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="js")
async def js_(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "js"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="show the leaderboard")
async def leaderboard(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "leaderboard"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="show your level")
async def level(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "level"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="list warnings")
async def listwarn(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "listwarn"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


@bot.SlashCommand.slash_command(description="show merch info")
async def merch(ctx: Context) -> None:

    server_id = str(ctx.guild.id)
    command_name = "merch"

    if not is_active_command(server_id, command_name):
        await ctx.send("https://cdn.discordapp.com/emojis/823403768448155648.webp")
    else:
        function_path = f"{FUNCTION_BASE_RUL}{command_name}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        data = {
            "server_id": server_id,
            "server_name": str(ctx.message.guild.name),
            "user_id": str(ctx.author.id),
            "username": str(ctx.author.name),
            "channel_id": str(ctx.channel.id),
            "message_id": str(ctx.message.id),
            "mentions": [str(user_id) for user_id in ctx.message.raw_mentions],
            "params": [],
        }

        response: Response = requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(data),
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


if __name__ == "__main__":

    cred = credentials.Certificate(KEY_FILE)
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    bot.remove_command("help")
    bot.run(DISCORD_API_TOKEN)
