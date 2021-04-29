import discord
from discord.ext import commands

from config.keys import PREFIX, CLIENT_ID, BOT_TOKEN#, BOT_ROOM_ID


EXTENSIONS = [
    'alldebrid',
    'bot_management',
    'custom_reactions',
    'greets',
    'music',
    'reaction_roles',
    'sns',
    'status',
    'utilities'
]


bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

for extension in EXTENSIONS:
    bot.load_extension(f'extensions.{extension}')
    print(f'Extension loaded: extensions.{extension}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print(discord.utils.oauth_url(CLIENT_ID))
    # bot_room = bot.get_channel(BOT_ROOM_ID)
    # await bot_room.send('ただいま〜')

bot.run(BOT_TOKEN)
