import discord
from discord.ext import commands

import json

from importlib import resources
import res
import saves


class Greets(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.guildpics = json.loads(resources.read_binary(saves, 'greets.json'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.system_channel is not None:
            try:
                with resources.path(res, self.guildpics[str(member.guild.id)]) as path:
                    file = discord.File(path)
            except KeyError:
                file = None
            await member.guild.system_channel.send(f'> Bienvenue {member.mention} !', file = file)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.system_channel is not None:
            await member.guild.system_channel.send('> **{0.name}#{0.discriminator}** nous a quitté.'.format(member))

    def cog_unload(self):
        with resources.path(saves, 'greets.json') as path:
            with open(path, 'w') as file:
                json.dump(self.guildpics, file, ensure_ascii=False, sort_keys=True, indent=4)


def setup(bot):
    bot.add_cog(Greets(bot))
