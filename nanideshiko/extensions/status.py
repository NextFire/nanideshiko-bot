import random

import discord
from discord.ext import commands, tasks

from ..utils.saves import sdump, sload


class Status(commands.Cog):
    SAVE_KEY = 'status'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.lstatus = sload(self.SAVE_KEY)
        self.loop_status.start()

    @tasks.loop(seconds=30)
    async def loop_status(self):
        activity = self.lstatus[random.randrange(len(self.lstatus))]
        await self.bot.change_presence(
            activity=discord.Activity(type=eval('discord.ActivityType.' +
                                                activity["type"]),
                                      name=activity["name"]))

    @loop_status.before_loop
    async def before_loop_status(self):
        await self.bot.wait_until_ready()

    @commands.command(aliases=['als'])
    @commands.is_owner()
    async def alstatus(self, ctx: commands.Context, type: str, *, name: str):
        """Adds status to loop list"""
        if type.lower() not in ('playing', 'listening', 'watching'):
            raise commands.CommandError(
                'Type should be playing, listening or watching')
        self.lstatus.append({"type": type.lower(), "name": name})
        await ctx.message.add_reaction('👌')

    @commands.command(aliases=['lls'])
    async def llstatus(self, ctx: commands.Context):
        """Shows loop status list"""
        lls = '```\n'
        for i in range(len(self.lstatus)):
            lls += f'{i}) ' + self.lstatus[i]["type"] + ' ' + self.lstatus[i][
                "name"] + '\n'
        lls += '```'
        await ctx.reply(lls)

    @commands.command(aliases=['rls'])
    @commands.is_owner()
    async def rlstatus(self, ctx: commands.Context, item: int):
        """Removes status of loop list"""
        self.lstatus.pop(item)
        await ctx.message.add_reaction('👌')

    def cog_unload(self):
        self.loop_status.cancel()
        sdump(self.SAVE_KEY, self.lstatus)


def setup(bot: commands.Bot):
    bot.add_cog(Status(bot))
