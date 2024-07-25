from __main__ import hexo
import discord
from discord.utils import get

meta = {
    "name": "Moderatio, Module",
    "id": "hera_moderation",
    "ver": "0.0.1",
    "desc": "Used for global moderation",
    "required": [],
    "author":"Herasium"
}

@hexo.client.tree.command(name="kick")
async def kick(ctx, member: discord.Member, *, reason: str=None):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    await member.kick(reason=reason)
    await ctx.response.send_message(f'User {member} have been kicked.',ephemeral = True)

@hexo.client.tree.command(name="mute")
async def mute(ctx, member: discord.Member,):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    guild = get(hexo.client.guilds, id=ctx.guild_id)
    role = get(guild.roles, id=1261990233155567690)

    if role in member.roles:
        await member.remove_roles(role)
    await member.add_roles(get(guild.roles, id=1262141857366806621))
    await ctx.response.send_message(f'User {member} has been muted.',ephemeral = True)

@hexo.client.tree.command(name="unmute")
async def unmute(ctx, member: discord.Member,):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    guild = get(hexo.client.guilds, id=ctx.guild_id)
    role = get(guild.roles, id=1262141857366806621)

    if role in member.roles:
        await member.remove_roles(role)
        await member.add_roles(get(guild.roles, id=1261990233155567690))
        
        await ctx.response.send_message(f'User {member} has been unmuted.',ephemeral = True)
    else:
        await ctx.response.send_message(f"User {member} wasn't muted.",ephemeral = True)

@hexo.client.tree.command(name="ban")
async def ban(ctx, member : discord.Member, reason:str = None):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    await member.ban(reason = reason)

@hexo.client.tree.command(name="warn")
async def warn(ctx, member : discord.Member):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    warn_ref = hexo.db.reference(f"/members/{member.id}/warn")
    warns = warn_ref.get()
    warns += 1
    warn_ref.set(warns)

    if warns == 3:
        await member.kick(reason="Kicked for 3 Warns")
        await ctx.response.send_message(f"User {member} got their third warn and has been kicked")
    elif warns == 5:
        await member.ban(reason="Banned for 5 Warns")
        await ctx.response.send_message(f"User {member} got their fifth warn and has been banned")
    else:
        await ctx.response.send_message(f"User {member} now have {warns} warn.")

@hexo.client.tree.command(name="unwarn")
async def unwarn(ctx, member : discord.Member):
    if not ctx.user.guild_permissions.administrator: 
        await hexo.not_permissions(ctx)
        return
    warn_ref = hexo.db.reference(f"/members/{member.id}/warn")
    warns = warn_ref.get()
    warns -= 1
    warn_ref.set(warns)

    await ctx.response.send_message(f"User {member} got removed 1 warn and is now at {warns} warns.")

@hexo.client.tree.command(name="warn_status")
async def warn_status(ctx, member : discord.Member):

    warn_ref = hexo.db.reference(f"/members/{member.id}/warn")
    warns = warn_ref.get()

    await ctx.response.send_message(f"User {member} have {warns} warn.")
    
@hexo.client.tree.command(name="clear")
async def clear(ctx, amount:int =None): 
    if not ctx.user.guild_permissions.administrator: 
        await hexo.not_permissions(ctx)
        return
    if amount == None:
        await ctx.channel.purge(limit=1000000)
    else:
        try:
            int(amount)
        except: # Error handler
            await ctx.response.send_message('Please enter a valid integer as amount.')
        else:
            await ctx.channel.purge(limit=amount)
            await ctx.response.send_message("Channel Cleared.",ephemeral = True)


functions = {}