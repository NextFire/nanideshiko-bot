import logging

import discord
from discord.ext import commands

from .config.settings import BOT_TOKEN, CLIENT_ID, LOG_LEVEL, PREFIX
from .extensions import load_extensions

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
load_extensions(bot)


@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
    logger.info(discord.utils.oauth_url(CLIENT_ID))


bot.run(BOT_TOKEN)
