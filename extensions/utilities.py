import discord
from discord.ext import commands


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
    async def avatar(self, ctx, user: discord.Member = None):
        """Gets <user> avatar"""
        if user is None:
            await ctx.reply(ctx.author.avatar_url)
        else:
            await ctx.reply(user.avatar_url)

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

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def move(self, ctx, destination: discord.TextChannel, start_msg_id: int):
        """Move entire connversations to another text channel
        
        Usage: `move #destination start_msg_id (@mentions)*`
        It will move all messages from @mentions (everybody if unspecified), after the provided start_msg_id (excluded), up to now, to #destination
        """
        async with ctx.channel.typing():
            webhook = await Utilities.get_webhook(destination)
            start_msg = await ctx.fetch_message(start_msg_id)
            if ctx.message.mentions != []:
                members = ctx.message.mentions
                unselected = False
            else:
                unselected = True
            async for message in ctx.channel.history(limit=None, after=start_msg, before=ctx.message, oldest_first=True):
                if unselected or (message.author in members):
                    try:
                        content = message.content
                    except:
                        content = None
                    try:
                        file =  await message.attachments[0].to_file()
                    except:
                        file = None
                    await webhook.send(content=content,
                                        embeds=message.embeds,
                                        file=file,
                                        username=message.author.display_name,
                                        avatar_url=message.author.avatar_url)
                    await message.delete()



def setup(bot):
    bot.add_cog(Utilities(bot))
