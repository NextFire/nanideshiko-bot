from importlib import resources

import discord
from discord.ext import commands

from ..config import res
from ..utils.saves import sdump, sload


class Greets(commands.Cog):
    SAVE_KEY = 'greets'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.guildpics = sload(self.SAVE_KEY)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild.system_channel is not None:
            try:
                with resources.path(res, self.guildpics[str(
                        member.guild.id)]) as path:
                    file = discord.File(path)
            except KeyError:
                file = None
            await member.guild.system_channel.send(
                f'> Bienvenue {member.mention} !', file=file)

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send(
                '> **{0.name}#{0.discriminator}** nous a quitté.'.format(member)
            )

    def cog_unload(self):
        sdump(self.SAVE_KEY, self.guildpics)


def setup(bot: commands.Bot):
    bot.add_cog(Greets(bot))
