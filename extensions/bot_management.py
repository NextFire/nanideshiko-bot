import discord
from discord.ext import commands


class BotManagement(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx: commands.Context, *, arg: str):
        """Sets the bot status"""
        self.bot.unload_extension('extensions.status')
        await self.bot.change_presence(activity=discord.Game(name=arg))
        await ctx.message.add_reaction('👌')
    
    @commands.command(aliases=['ls'])
    @commands.is_owner()
    async def lstatus(self, ctx: commands.Context):
        """Activates loop status"""
        self.bot.load_extension('extensions.status')
        await ctx.message.add_reaction('👌')

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx: commands.Context, extension: str):
        """Reloads an <extension>"""
        self.bot.reload_extension(f'extensions.{extension}'.lower())
        await ctx.message.add_reaction('👌')

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx: commands.Context, extension: str):
        """Unloads an <extension>"""
        self.bot.unload_extension(f'extensions.{extension}'.lower())
        await ctx.message.add_reaction('👌')

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx: commands.Context, extension: str):
        """Loads an <extension>"""
        self.bot.load_extension(f'extensions.{extension}'.lower())
        await ctx.message.add_reaction('👌')


def setup(bot: commands.Bot):
    bot.add_cog(BotManagement(bot))
