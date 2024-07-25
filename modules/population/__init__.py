from __main__ import hexo
import discord
from discord.utils import get

meta = {
    "name": "Population Module",
    "id": "hera_pop",
    "ver": "0.0.1",
    "desc": "Used to set the member count.",
    "required": [],
    "author":"Herasium"
}

async def set_info_name():
    guild = get(hexo.client.guilds, id=hexo.data["guild_id"]) 
    channel = hexo.client.get_channel(hexo.data["nfo_category_id"])
    await channel.edit(name=f"INFO - {'{:,}'.format(guild.member_count)} Members")


@hexo.client.tree.command(name="update_info_name")
async def update_info_name(ctx):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    await set_info_name()
    await ctx.response.send_message("Updated Info Name",ephemeral = True)


functions = {
    "on_join": set_info_name,
    "on_leave": set_info_name
}