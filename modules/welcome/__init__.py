from __main__ import hexo
import random


welcome_sentences = [
    ["Hello World "," !"],
    [""," made the right choice in life!"],
    [""," is now in the best discord server ever!!!!!!!!!"],
    ["I hope you got pizzas "," ! :pizza:"],
    ["A wild "," just spawned !"],
]

goodbye_sentences = [
    [""," just vanished :("],
    [""," made the wrong choice in life"],
    ["Rip, "," just left :("],
    ["Can someone help "," come back ?"], 
    [""," doesn't have internet anymore"],
]

async def welcome(member):
    welcome_id = hexo.client.get_channel(hexo.data["welcome_channel_id"])
    sentence = random.choice(welcome_sentences)
    await welcome_id.send(content = "<:enter:1261985388088660039> "+sentence[0]+member.mention+sentence[1])
 
async def goodbye(member):
    welcome_id = hexo.client.get_channel(hexo.data["welcome_channel_id"])
    sentence = random.choice(goodbye_sentences)
    await welcome_id.send(content = "<:leave:1261985403624230942> "+sentence[0]+member.mention+sentence[1])


functions = {
    "on_join":welcome,
    "on_leave":goodbye,
}