import re

import discord
from discord.ext import commands

from ..utils.saves import sdump, sload


class CustomReactions(commands.Cog):
    SAVE_KEY = 'custom_reactions'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.triggers = sload(self.SAVE_KEY)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.bot.user:
            return
        if message.content[:0] == self.bot.command_prefix:
            return
        for trigger in self.triggers["exact"]:
            if message.content.lower() == trigger.lower():
                await message.channel.send(self.triggers["exact"][trigger])
                return
        for trigger in self.triggers["partial"]:
            if re.search(rf'\b{trigger}\b'.lower(), message.content.lower()):
                await message.channel.send(self.triggers["partial"][trigger])

    @commands.command()
    @commands.is_owner()
    async def acr(self,
                  ctx: commands.Context,
                  trigger: str,
                  response: str,
                  mode: str = "partial"):
        """Adds custom reaction
        mode is partial or exact"""
        mode = mode.lower()
        if mode not in ("exact", "partial"):
            raise commands.CommandError('Mode should be exact or partial')
        self.triggers[mode][trigger] = response
        await ctx.message.add_reaction('👌')

    @commands.command()
    @commands.is_owner()
    async def dcr(self, ctx: commands.Context, trigger: str, mode: str = None):
        """Deletes custom reaction
        mode is partial or exact"""
        if mode not in (None, "exact", "partial"):
            raise commands.CommandError('Mode should be None, exact or partial')
        if mode is None:
            for mode in ("exact", "partial"):
                self.triggers[mode].pop(trigger, None)
        else:
            self.triggers[mode].pop(trigger, None)
        await ctx.message.add_reaction('👌')

    @commands.command()
    async def lcr(self, ctx: commands.Context):
        """Lists custom reactions"""
        lcr = '```\n'
        for mode in ("exact", "partial"):
            lcr += mode + '\n'
            for trigger in self.triggers[mode]:
                lcr += '\t' + trigger + '\n'
            lcr += '\n'
        lcr += '```'
        await ctx.reply(lcr)

    def cog_unload(self):
        sdump(self.SAVE_KEY, self.triggers)


def setup(bot: commands.Bot):
    bot.add_cog(CustomReactions(bot))
