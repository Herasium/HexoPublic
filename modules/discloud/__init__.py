import requests
from __main__ import hexo


meta = {
    "name": "Discloud Module",
    "id": "hera_discloud",
    "ver": "0.0.1",
    "desc": "Deal with the host for the /restart command",
    "required": [],
    "author":"Herasium"
}

token = hexo.secrets["discloud"]
url = "https://api.discloud.app/v2/"
headers = {"api-token":token}


def get_current_app_id():
    data = requests.get(url+"user",headers=headers).json()
    return data["user"]["apps"][0]

app_id = get_current_app_id()

def restart_app():
    hexo.logger.info("Restarting App")
    data = requests.put(url+"app/"+app_id+"/restart",headers=headers).json()
    if data.status == "ok":
        hexo.logger.info("Restarted App :thumbs_up:")
    else:
        hexo.logger.error("Failed to restart app:"+data.message)

@hexo.client.tree.command(name="restart")
async def unwarn(ctx):
    if not ctx.user.guild_permissions.administrator: 
        await hexo.not_permissions(ctx)
        return
    await ctx.response.send_message(f"Restart attemp launched. Please see #log",ephemeral = True)
    restart_app()
    

functions = {}