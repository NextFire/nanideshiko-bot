import asyncio
import logging
import re
from datetime import datetime
from time import mktime

import aiohttp
import discord
import feedparser
from discord.ext import commands
from html2text import HTML2Text

from ..config.settings import RSS_CHANNEL_ID
from ..utils.saves import sload

logger = logging.getLogger(__name__)

html2text = HTML2Text()
html2text.body_width = 0
html2text.single_line_break = True


class RSS(commands.Cog):
    SAVE_KEY = 'rss'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.process_task = None
        self.feeds = sload(self.SAVE_KEY)
        self.last_update = datetime.utcnow()
        self.send_lock = asyncio.Lock()

    @commands.Cog.listener()
    async def on_ready(self):
        if self.process_task is None:
            self.process_task = asyncio.create_task(self.process())

    def cog_unload(self):
        if self.process_task is not None:
            self.process_task.cancel()

    async def process(self):
        async with aiohttp.ClientSession() as session:
            while True:
                logger.info('Processing RSS feeds')
                for feed in self.feeds:
                    asyncio.create_task(self.process_feed(feed, session))
                await asyncio.sleep(3600)

    async def process_feed(self, feed: dict, session: aiohttp.ClientSession):
        async with session.get(feed['url']) as resp:
            text = await resp.text()
        data = feedparser.parse(text)

        new_entries = [
            e for e in data.entries if datetime.utcfromtimestamp(
                mktime(e.published_parsed)) > self.last_update
        ]
        self.last_update = datetime.utcnow()

        if new_entries and feed['filter'] is not None:
            regex = re.compile(fr"\b{feed['filter']}\b", re.IGNORECASE)
            new_entries = [e for e in new_entries if regex.search(e.title)]

        if new_entries:
            asyncio.create_task(self.send(data, new_entries))

    async def send(self, data: dict, entries: list[dict]):
        embeds = await asyncio.gather(
            *(self.get_embed(data, e) for e in reversed(entries)))
        chan: discord.TextChannel = self.bot.get_channel(RSS_CHANNEL_ID)
        async with self.send_lock:
            for em in embeds:
                await chan.send(embed=em)

    async def get_embed(self, data: dict, entry: dict):
        embed = discord.Embed()
        embed.title = entry.title
        embed.url = entry.link
        embed.description = html2text.handle(entry.summary)
        return embed


def setup(bot: commands.Bot):
    bot.add_cog(RSS(bot))
