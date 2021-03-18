import discord
from discord.ext import commands

import aiohttp
import asyncio

from keys import AD_USER_AGENT, AD_API_KEY


AD_MAGNET_UPLOAD_URL = 'https://api.alldebrid.com/v4/magnet/upload'
AD_MAGNET_STATUS_URL = 'https://api.alldebrid.com/v4/magnet/status'
AD_LINK_UNLOCK_URL = 'https://api.alldebrid.com/v4/link/unlock'
AD_AUTH = {'agent': AD_USER_AGENT, 'apikey': AD_API_KEY}


class AlldebridRequests:

    async def alldebrid_magnet_upload(session: aiohttp.ClientSession, magnet: str) -> dict:
        async with session.get(AD_MAGNET_UPLOAD_URL, params={**AD_AUTH, 'magnets[]': magnet}) as resp:
            return (await resp.json())['data']['magnets'][0]

    async def alldebrid_magnet_status(session: aiohttp.ClientSession, magnet_id: int) -> dict:
        async with session.get(AD_MAGNET_STATUS_URL, params={**AD_AUTH, 'id': magnet_id}) as resp:
            return (await resp.json())['data']['magnets']

    async def alldebrid_link_unlock(session: aiohttp.ClientSession, link: str) -> str:
        async with session.get(AD_LINK_UNLOCK_URL, params={**AD_AUTH, 'link': link}) as resp:
            return (await resp.json())['data']


class Alldebrid(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def magnet(self, ctx: commands.Context, *, magnet: str):
        """Magnet -> DDL"""
        async with aiohttp.ClientSession() as session:
            ad_magnet = await AlldebridRequests.alldebrid_magnet_upload(session, magnet)
            message = await ctx.send(embed=discord.Embed(title=ad_magnet['name'], description=f"`[{'▒' * 20}] 0.0%`"))
            status = ''
            while status != 'Ready':
                await asyncio.sleep(1)
                ad_magnet = await AlldebridRequests.alldebrid_magnet_status(session, ad_magnet['id'])
                status = ad_magnet['status']
                percentage = 100 * ad_magnet['downloaded']/ad_magnet['size'] if ad_magnet['size'] != 0 else 0
                if percentage < 100:
                    await message.edit(embed=discord.Embed(title=ad_magnet['filename'], description=f"`[{'█' * int(percentage / 5)}{'▒' * (20 - int(percentage / 5))}] {percentage:.1f}%`"))
                else:
                    await message.edit(embed=discord.Embed(title=ad_magnet['filename'], description=f"`[{'█'*20}] 100.0%`\nUploading to Uptobox"))
            embed = discord.Embed()
            for item in ad_magnet['links']:
                unlocked = await AlldebridRequests.alldebrid_link_unlock(session, item['link'])
                embed.add_field(name=unlocked['filename'], value=f"[Link]({unlocked['link']})")
            await message.edit(embed=embed)


def setup(bot: commands.Bot):
    bot.add_cog(Alldebrid(bot))

