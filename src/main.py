import json
import logging
import os
import re

import google.oauth2.id_token
import requests
from discord import Embed
from discord.ext.commands import Bot, Context
from discord.message import Message as message_type
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from requests import Response

load_dotenv()

LOGGER: logging.Logger = logging.getLogger(__name__)
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")
FUNCTION_BASE_RUL = "https://us-central1-archy-f06ed.cloudfunctions.net/"

# Discord bot settings
bot: Bot = Bot(command_prefix="!", description="Serverless commands discord bot")

# Gcloud auth settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"
request = Request()


@bot.event
async def on_message(message: message_type) -> None:
    LOGGER.warning("Message from %s is: %s", message.author, message.content)

    ctx: Context = await bot.get_context(message)
    if ctx.invoked_with:
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
                    "user_id": str(ctx.author.id),
                    "username": str(ctx.author.name),
                    "channel_id": str(message.channel.id),
                    "message_id": str(message.id),
                    "mentions": ctx.message.raw_mentions,
                    "params": message.content.split(ctx.command)[1:],
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
        function_path = f"{FUNCTION_BASE_RUL}exp"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)

        requests.post(
            function_path,
            headers={
                "Authorization": f"Bearer {google_auth_token}",
                "Content-Type": "application/json",
            },
            data=json.dumps(
                {
                    "server_id": str(ctx.guild.id),
                    "user_id": str(ctx.author.id),
                    "username": str(ctx.author.name),
                    "avatar_url": f"{ctx.author.avatar_url.BASE}{ctx.author.avatar_url._url}",  # pylint: disable=W0212
                }
            ),
        )

    # Simple interaction when a user send "@bot_name"
    if message.content == f"<@{bot.user.id}>":
        await ctx.send("> Who Dares Summon Me?")


@bot.event
async def on_message_edit(before: message_type, after: message_type) -> None:
    LOGGER.warning(before)
    LOGGER.warning(after)


bot.remove_command("help")
bot.run(DISCORD_API_TOKEN)
