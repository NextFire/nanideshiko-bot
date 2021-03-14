import discord
from discord.ext import commands

import datetime
import random
import re

import asyncpraw

from extensions.utilities import Utilities
from keys import PREFIX, REDDIT_CLIENT_ID, REDDIT_SECRET, REDDIT_USER_AGENT, REDDIT_USERNAME, REDDIT_PASSWORD


class RedditCommands(commands.Cog, name='Reddit Commands'):

    reddit = asyncpraw.Reddit(client_id=REDDIT_CLIENT_ID,
                            client_secret=REDDIT_SECRET,
                            user_agent=REDDIT_USER_AGENT,
                            username=REDDIT_USERNAME,
                            password=REDDIT_PASSWORD)

    def __init__(self, bot):
        self.bot = bot

    async def _send_embed(self, ctx, post: asyncpraw.models.Submission, content: str = None, webhook_enabled = False):
        await post.subreddit.load()
        await post.author.load()
        if post.over_18 and post.spoiler:
            description = '`[NSFW][SPOILER]`'
        elif post.over_18:
            description = '`[NSFW]`'
        elif post.spoiler:
            description = '`[SPOILER]`'
        else:
            if len(post.selftext) > 2048:
                description = post.selftext[:(2048-20)] + '\n\n`[TRUNCATED POST]`'
            else:
                description = post.selftext
        embed = discord.Embed(colour= 0xFF4500,
                                title = post.title,
                                description = description,
                                timestamp=datetime.datetime.fromtimestamp(post.created_utc),
                                url=f'https://www.reddit.com{post.permalink}')
        if post.url[-3:] in ('jpg', 'png'):
            if post.over_18 or post.spoiler:
                embed.set_image(url=post.preview['images'][0]['variants']['obfuscated']['source']['url'])
            else:
                embed.set_image(url=post.url)
        embed.set_author(name=f'r/{post.subreddit}', url=f'https://www.reddit.com/r/{post.subreddit}', icon_url=post.subreddit.icon_img)
        embed.set_footer(text=f'u/{post.author.name} on reddit', icon_url=post.author.icon_img)
        embed.add_field(name=f'🔺 Upvotes', value=post.score)
        embed.add_field(name=f'💬 Comments', value=post.num_comments)
        if webhook_enabled:
            webhook = await Utilities.get_webhook(ctx.channel)
            await webhook.send(content=content, embed=embed,
                                username=ctx.author.display_name,
                                avatar_url=ctx.author.avatar_url)
        else:
            await ctx.send(content=content, embed=embed)

    @commands.command()
    async def hug(self, ctx, user: discord.Member = None):
        """Par le pouvoir du moe"""
        awwnime = await self.reddit.subreddit('awwnime')
        await awwnime.load()
        results = []
        async for result in awwnime.search('hug'):
            results.append(result)
        n = random.randrange(len(results))
        post = results[n]
        if user is not None:
            content = f'🐰 {ctx.author.mention} hugged {user.mention}'
        else:
            content = f'🐰 Hugged {ctx.author.mention}'
        await self._send_embed(ctx, post, content)
        await ctx.message.delete()

    @commands.command()
    async def aww(self, ctx):
        """Get random hot r/awwnime post"""
        awwnime = await self.reddit.subreddit('awwnime')
        await awwnime.load()
        results = []
        async for result in awwnime.hot():
            results.append(result)
        n = random.randrange(len(results))
        post = results[n]
        await self._send_embed(ctx, post, '*aww*')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.content[:len(PREFIX)] == PREFIX:
            return
        if re.search(r"(reddit.com/r/[^ ]+/comments)", message.content) is not None:
            message_ctx = await self.bot.get_context(message)
            post = await self.reddit.submission(url=re.search(r"(https://[^ ?]+)", message.content).group(1))
            await message.delete()
            await self._send_embed(message_ctx, post, message.content, True)


def setup(bot):
    bot.add_cog(RedditCommands(bot))
