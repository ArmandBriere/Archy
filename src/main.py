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
FUNCTION_BASE_RUL = "https://us-central1-archy-f06ed.cloudfunctions.net/archy_py"
GOOGLE_AUTH_TOKEN = google.oauth2.id_token.fetch_id_token(request, FUNCTION_BASE_RUL)


@bot.command()
async def hello(ctx: context_type):
    r = requests.post(
        "https://us-central1-archy-f06ed.cloudfunctions.net/archy_py",
        headers={"Authorization": f"Bearer {GOOGLE_AUTH_TOKEN}", "Content-Type": "application/json"},
        data=json.dumps({"name": str(ctx.author)}),
    )
    await ctx.send(r.content.decode("utf-8"))


@bot.event
async def on_message(message: message_type):
    logger.warning("Message from %s is: %s", message.author, message.content)

    await bot.process_commands(message)


@bot.event
async def on_message_edit(before: message_type, after: message_type):
    logger.warning(before)
    logger.warning(after)


cog_files = ["functions.test"]

for cog_file in cog_files:
    bot.load_extension(cog_file)
    print(f"{cog_file} has loaded.")

bot.run(DISCORD_API_TOKEN)
