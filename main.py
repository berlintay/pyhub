import discord
from discord.ext import commands
import os
import asyncio
import logging
from logging.handlers import RotatingFileHandler
from discord.ext.commands import errors
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    filename='bot.log',
    encoding='utf-8',
    maxBytes=32 * 1024 * 1024,
    backupCount=5
)
dt_fmt = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(
    '[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
MESSAGE_CHANNEL_ID = int(os.getenv("MESSAGE_CHANNEL_ID"))


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                logging.info(f"Loaded cog: {filename[:-3]}")
            except (errors.ExtensionNotFound, errors.ExtensionFailed) as e:
                logging.error(f"Failed to load cog '{filename[:-3]}': {e}")


@bot.event
async def on_ready():
    await load_cogs()
    await bot.tree.sync()
    logging.info(f'Logged in as {bot.user.name} (ID: {bot.user.id})')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You have no perms to use this command.")
    else:
        logging.error(f"An error occurred: {error}")
        await ctx.send("An error occurred while processing this command...")

bot.run(TOKEN)
