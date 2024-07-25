from __main__ import hexo
import discord
import time
import random
import math
from StringProgressBar import progressBar


level_messages = [
    ["Level Up "," !"],
    ["GG "," you just leveled up !"],
    [""," is very active ! :)"],
    ["Pretty sure that "," is alive !"]
]

async def new_message(message):
    
    member = message.author
    
    last_ref = hexo.db.reference(f"/members/{member.id}/last_mess_time")
    last_mess = last_ref.get()
    last_ref.set(time.time())
    if last_mess+3 > time.time() : return

    level = hexo.db.reference(f"/members/{member.id}/level").get()
    xp = hexo.db.reference(f"/members/{member.id}/xp").get()
    required_xp = ((level*(level/2))+1*100)

    given_xp = 5 + random.randint(-1,3)
    
    if xp+given_xp >= required_xp:
        hexo.db.reference(f"/members/{member.id}/level").set(level + 1)
        hexo.db.reference(f"/members/{member.id}/xp").set((xp+given_xp) - required_xp)

        await level_up_message(member,level+1)
    else: 
        hexo.db.reference(f"/members/{member.id}/xp").set(xp+given_xp)

async def level_up_message(member,level):

    sentence = random.choice(level_messages)
    text = sentence[0] + "**" + member.name + "**" + sentence[1] + " *Level "+str(level-1)+"*  <:enter:1261985388088660039>  **Level "+str(level)+"**"
    channel = hexo.client.get_channel(hexo.data["level_channel_id"])
    await channel.send(content = text)


@hexo.client.tree.command(name="level")
async def level_profile(ctx):
    member = ctx.user

    level = hexo.db.reference(f"/members/{member.id}/level").get()
    xp = hexo.db.reference(f"/members/{member.id}/xp").get()
    required_xp = ((level*(level/2))+1*100)
    missing_xp = required_xp - xp
    min_messages = math.floor(missing_xp/8)
    max_messages = math.floor(missing_xp/4)
    bar = progressBar.filledBar(int(math.floor(required_xp)), int(math.floor(xp)),size=13,line="░",slider="█")

    embed=discord.Embed(title=f"Level {level}")
    embed.set_author(name=ctx.user.name,icon_url=ctx.user.avatar)
    embed.add_field(name=f"{xp} / {required_xp}xp", value=f"{bar[0]} {math.floor(bar[1])}%", inline=False)
    embed.set_footer(text=f"{min_messages} ~ {max_messages} messages left")
    await ctx.response.send_message(embed=embed)

@hexo.client.tree.command(name="leaderboard")
async def leaderboard_command(ctx):
        ref = hexo.db.reference('/members')
        members = ref.get()
        sorted_members = sorted(members.items(), key=lambda item: item[1].get('level', 0), reverse=True)
        top_10_members = sorted_members[:10]
        
        embed=discord.Embed(title="XP Leaderboard")
        count = 1
        for i in top_10_members:
            embed.add_field(name=f"{count}. {i[1]['name']} - Level {i[1]['level']}", value="", inline=False)
            count += 1
        await ctx.response.send_message(embed=embed)

functions = {
    "on_message":new_message
}