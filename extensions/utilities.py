import discord
from discord.ext import commands

import asyncio
import typing


async def run(cmd: str):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    if stderr:
        raise commands.CommandError(stderr.decode())

    return stdout.decode() if stdout else None


class Utilities(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    async def get_webhook(channel: discord.TextChannel):
        webhooks = await channel.webhooks()
        if webhooks:
            return webhooks[0]
        else:
            return await channel.create_webhook(name="nanideshiko")

    @commands.command()
    async def ping(self, ctx):
        """Bot ping test"""
        pong = await ctx.send('🏓')
        ping = ctx.message
        await ctx.send('`' + str(int(pong.created_at.timestamp() * 1000) - int(ping.created_at.timestamp() * 1000)) + ' ms`')

    @commands.command(aliases=['prune'])
    @commands.is_owner()
    async def rm(self, ctx, number):
        """Removes last <number> msgs"""
        msgs = []  # Empty list to put all the messages in the log
        # Converting the amount of messages to delete to an integer
        number = int(number)
        async for x in ctx.message.channel.history(limit=number + 1):
            msgs.append(x)
        await ctx.channel.delete_messages(msgs)

    @commands.command(hidden=True, aliases=['send'])
    @commands.is_owner()
    async def say(self, ctx, id, *, msg):
        """Sends <msg> to channel <id> with this bot"""
        channel = self.bot.get_channel(int(id))
        await channel.send(msg)

    @commands.command(aliases=['url', 'avatar'])
    async def link(self, ctx: commands.Context, user_or_emoji: typing.Union[discord.User, discord.PartialEmoji] = None):
        """Get an user or custom emoji link."""
        if isinstance(user_or_emoji, discord.PartialEmoji):
            await ctx.reply(user_or_emoji.url)
        else:
            await ctx.reply((user_or_emoji or ctx.author).avatar_url)

    @commands.command(name='import')
    async def emoji_import(self, ctx: commands.Context, emoji: discord.PartialEmoji, name: str = None):
        """Import a custom emoji."""
        imported = await ctx.guild.create_custom_emoji(name=name or emoji.name, image=await emoji.url.read())
        await ctx.reply(imported)

    @commands.command()
    @commands.is_owner()
    async def speedtest(self, ctx: commands.Context):
        """Run speedtest on the hosting device."""
        async with ctx.typing():
            result = await run('speedtest')
        await ctx.reply('```' + result + '```')


def setup(bot):
    bot.add_cog(Utilities(bot))
