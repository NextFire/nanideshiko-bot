import discord
from discord.ext import commands

from ..utils.saves import sdump, sload


class ReactionRoles(commands.Cog):
    SAVE_KEY = 'reaction_roles'

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.msgs = sload(self.SAVE_KEY)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self,
                                  payload: discord.RawReactionActionEvent):
        if str(payload.message_id) in list(self.msgs):
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(
                int(self.msgs[str(payload.message_id)][str(payload.emoji.id)]))
            member = guild.get_member(payload.user_id)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self,
                                     payload: discord.RawReactionActionEvent):
        if str(payload.message_id) in list(self.msgs):
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(
                int(self.msgs[str(payload.message_id)][str(payload.emoji.id)]))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)

    def cog_unload(self):
        sdump(self.SAVE_KEY, self.msgs)


def setup(bot: commands.Bot):
    bot.add_cog(ReactionRoles(bot))
