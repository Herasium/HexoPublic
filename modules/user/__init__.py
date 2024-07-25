from __main__ import hexo
import discord
import time

meta = {
    "name": "UserData Module",
    "id": "hera_user",
    "ver": "0.0.1",
    "desc": "User Data DB Handler",
    "required": [],
    "author":"Herasium"
}

async def add_user(member):
    
    user_ref = hexo.db.reference(f"/members/{member.id}")
    user_data = user_ref.get()

    if user_data != None:
        hexo.db.reference(f"/members/{member.id}/in_server").set(True)
        hexo.db.reference(f"/members/{member.id}/joined_number").set(hexo.db.reference(f"/members/{member.id}/joined_number").get()+1)
        hexo.db.reference(f"/members/{member.id}/joined_time").set(time.time())
        return
    
    generated_data = {
        "name":member.name,
        "id":member.id,
        "mention":member.mention,
        "level":0,
        "xp":0,
        "joined_time": time.time(),
        "joined_number":1,
        "leaved_number":0,
        "in_server":True,
        "warn":0,
        "ban":False,
        "ban_until":None,
        "hexa_connected":False,
        "hexa_acc":None,
        "last_mess_time":0,
        "muted":False,
        "muted_until":None,
        "data_ver":1,
        "bot_ver":1
    }

    user_ref.set(generated_data)


async def user_leave(member):

    hexo.db.reference(f"/members/{member.id}/in_server").set(False)
    hexo.db.reference(f"/members/{member.id}/leaved_number").set(hexo.db.reference(f"/members/{member.id}/leaved_number").get()+1)
   

@hexo.client.tree.command(name="create_user_profile_db")
async def create_profile(ctx,user: discord.Member):
    if not ctx.user.guild_permissions.administrator: 
         await hexo.not_permissions(ctx)
         return
    await add_user(user)
    await ctx.response.send_message("Created Profile",ephemeral = True)
    
functions = {
    "on_join":add_user,
    "on_leave":user_leave
}