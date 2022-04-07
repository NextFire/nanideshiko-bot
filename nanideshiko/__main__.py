import logging

import discord
from discord.ext import commands

from .config.settings import BOT_TOKEN, LOG_LEVEL, PREFIX
from .extensions import load_extensions

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())
load_extensions(bot)
bot.run(BOT_TOKEN)
