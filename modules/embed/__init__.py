from __main__ import hexo
import discord

meta = {
    "name": "Embed Module",
    "id": "hera_embed",
    "ver": "0.0.1",
    "desc": "Simple Embed Command",
    "required": [],
    "author":"Herasium"
}

@hexo.client.tree.command(name="embed") 
async def embed_custom(ctx: discord.Interaction, title: str, description: str, color: str): 
  try:
      embed = discord.Embed(
        title=title,
        description=description,
        color=int(f"0x{color}",16))
      await ctx.response.send_message(embed=embed) 
  except Exception:
      embed=discord.Embed(title="Error", color=0xff0000)
      embed.add_field(name=f"There was an error generating you response, please try again later.", value="", inline=False)
      await ctx.response.send_message(embed=embed) 


functions = {}