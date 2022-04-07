import discord
from discord.ext import commands


class Utilities(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        """Bot ping test"""
        pong = await ctx.send('🏓')
        ping = ctx.message
        await ctx.send('`' + str(
            int(pong.created_at.timestamp() * 1000) -
            int(ping.created_at.timestamp() * 1000)) + ' ms`')

    @commands.command(aliases=['prune'])
    @commands.is_owner()
    async def rm(self, ctx: commands.Context, number: int):
        """Removes last <number> msgs"""
        msgs = []  # Empty list to put all the messages in the log
        # Converting the amount of messages to delete to an integer
        async for x in ctx.message.channel.history(limit=number + 1):
            msgs.append(x)
        await ctx.channel.delete_messages(msgs)

    @commands.command(hidden=True, aliases=['send'])
    @commands.is_owner()
    async def say(self, ctx: commands.Context, id: int, *, msg: str):
        """Sends <msg> to channel <id> with this bot"""
        channel = self.bot.get_channel(id)
        await channel.send(msg)

    @commands.command(aliases=['url', 'avatar'])
    async def link(self,
                   ctx: commands.Context,
                   user_or_emoji: discord.User | discord.PartialEmoji = None):
        """Get an user or custom emoji link."""
        if isinstance(user_or_emoji, discord.PartialEmoji):
            await ctx.reply(user_or_emoji.url)
        else:
            await ctx.reply((user_or_emoji or ctx.author).avatar_url)

    @commands.command(name='import')
    async def emoji_import(self,
                           ctx: commands.Context,
                           emoji: discord.PartialEmoji,
                           name: str = None):
        """Import a custom emoji."""
        imported = await ctx.guild.create_custom_emoji(name=name or emoji.name,
                                                       image=await
                                                       emoji.url.read())
        await ctx.reply(imported)


def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
