import platform
from __main__ import hexo
import discord

meta = {
    "name": "Status Module",
    "id": "hera_status",
    "ver": "0.0.1",
    "desc": "Deal With Status",
    "required": [],
    "author":"Herasium"
}

@hexo.client.tree.command(name="host")
async def current_host(ctx):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    await ctx.response.send_message("Current Host: "+platform.system()+" "+platform.release())
 
@hexo.client.tree.command(name="status")
async def status(ctx):   
    modules = hexo.modules
    text = ""
    
    for module in modules:
        if modules[module]["loaded"]:
            text += "<:enter:1261985388088660039> "
        else:
            text += "<:leave:1261985403624230942> "
        text += modules[module]["id"] + "\n"
    
    embed=discord.Embed(title="Bot Status", description="Seems fine for me")
    embed.add_field(name="Host", value=platform.system()+" "+platform.release(), inline=False)
    embed.add_field(name="Modules", value=text, inline=True)
    
    await ctx.response.send_message(embed=embed)
    

functions = {}
