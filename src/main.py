import os
import json
import requests
import google.oauth2.id_token
import google.auth.transport.requests

import logging

from discord.message import Message as message_type
from discord.ext.commands.context import Context as context_type

from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# Discord bot settings
bot = commands.Bot(command_prefix="!", description="Serverless commands discord bot")
DISCORD_API_TOKEN = os.getenv("DISCORD_API_TOKEN")

# Gcloud auth settings
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./key.json"
request = google.auth.transport.requests.Request()
FUNCTION_BASE_RUL = "https://us-central1-archy-f06ed.cloudfunctions.net/"


@bot.event
async def on_message(message: message_type):
    logger.warning("Message from %s is: %s", message.author, message.content)

    ctx = await bot.get_context(message)
    print(f"invoked with {ctx.invoked_with}")

    if ctx.invoked_with:
        function_path = f"{FUNCTION_BASE_RUL}{ctx.invoked_with}"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)
        r = requests.post(
            function_path,
            headers={"Authorization": f"Bearer {google_auth_token}", "Content-Type": "application/json"},
            data=json.dumps({"name": str(ctx.author.id)}),
        )

        if r.status_code == 200:
            await ctx.send(r.content.decode("utf-8"))

    elif not message.author.bot:
        function_path = f"{FUNCTION_BASE_RUL}exp"
        google_auth_token = google.oauth2.id_token.fetch_id_token(request, function_path)
        r = requests.post(
            function_path,
            headers={"Authorization": f"Bearer {google_auth_token}", "Content-Type": "application/json"},
            data=json.dumps({"name": str(ctx.author.id)}),
        )
        await ctx.send(r.content.decode("utf-8"))


@bot.event
async def on_message_edit(before: message_type, after: message_type):
    logger.warning(before)
    logger.warning(after)


cog_files = ["functions.test"]

for cog_file in cog_files:
    bot.load_extension(cog_file)
    print(f"{cog_file} has loaded.")

bot.run(DISCORD_API_TOKEN)
