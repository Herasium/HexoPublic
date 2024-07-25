from __main__ import hexo
import discord
from discord.utils import get

meta = {
    "name": "Role React Module",
    "id": "hera_rreact",
    "ver": "0.0.1",
    "desc": "Used for role react purposes",
    "required": [],
    "author":"Herasium"
}

reactions_buffer = hexo.db.reference("/role_react").get()

if reactions_buffer == None:
    reactions_buffer = {}

@hexo.client.tree.command(name="role_react")
async def react_rules(ctx,message: str,emojie: str, role: discord.Role, let_reaction: bool):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    generated_data = {
        "message":message,
        "emojie":emojie,
        "role":role.id,
        "let_reaction":let_reaction,
    }

    hexo.db.reference("/role_react/"+str(message)).set(generated_data)
    msg = await ctx.channel.fetch_message(message)
    reactions_buffer = hexo.db.reference("/role_react").get() 
    await msg.add_reaction(emojie)

    await ctx.response.send_message("Added Reaction",ephemeral = True)


@hexo.client.event
async def on_raw_reaction_add(reaction):
    guild = get(hexo.client.guilds, id=reaction.guild_id)

    if str(reaction.message_id) in reactions_buffer:
        if reactions_buffer[str(reaction.message_id)]["emojie"] == reaction.emoji.name:
            await guild.get_member(reaction.user_id).add_roles(get(guild.roles, id=reactions_buffer[str(reaction.message_id)]["role"]))

@hexo.client.event
async def on_raw_reaction_remove(reaction):

    guild = get(hexo.client.guilds, id=reaction.guild_id)
    user =  guild.get_member(reaction.user_id)

    if str(reaction.message_id) in reactions_buffer:
        if reactions_buffer[str(reaction.message_id)]["emojie"] == reaction.emoji.name:
            role = get(guild.roles, id=reactions_buffer[str(reaction.message_id)]["role"]) 
            if role in user.roles:
                await user.remove_roles(role)


functions = {}