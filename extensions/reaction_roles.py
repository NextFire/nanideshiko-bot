from discord.ext import commands

import json

from importlib import resources
import config.saves


class ReactionRoles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.msgs = json.loads(resources.read_binary(config.saves, 'reaction_roles.json'))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if str(payload.message_id) in list(self.msgs):
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(self.msgs[str(payload.message_id)][str(payload.emoji.id)]))
            member = guild.get_member(payload.user_id)
            await member.add_roles(role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if str(payload.message_id) in list(self.msgs):
            guild = self.bot.get_guild(payload.guild_id)
            role = guild.get_role(int(self.msgs[str(payload.message_id)][str(payload.emoji.id)]))
            member = guild.get_member(payload.user_id)
            await member.remove_roles(role)

    def cog_unload(self):
        with resources.path(config.saves, 'reaction_roles.json') as path:
            with open(path, 'w') as file:
                json.dump(self.msgs, file, ensure_ascii=False, indent=4)


def setup(bot):
    bot.add_cog(ReactionRoles(bot))
