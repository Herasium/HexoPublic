from __main__ import hexo
import discord
import random

hiragana_to_romaji = {
    "あ": "a",
    "い": "i",
    "う": "u",
    "え": "e",
    "お": "o",
    "か": "ka",
    "き": "ki",
    "く": "ku",
    "け": "ke",
    "こ": "ko",
    "さ": "sa",
    "し": "shi",
    "す": "su",
    "せ": "se",
    "そ": "so",
    "た": "ta",
    "ち": "chi",
    "つ": "tsu",
    "て": "te",
    "と": "to",
    "な": "na",
    "に": "ni",
    "ぬ": "nu",
    "ね": "ne",
    "の": "no",
    "は": "ha",
    "ひ": "hi",
    "ふ": "fu",
    "へ": "he",
    "ほ": "ho",
    "ま": "ma",
    "み": "mi",
    "む": "mu",
    "め": "me",
    "も": "mo",
    "や": "ya",
    "ゆ": "yu",
    "よ": "yo",
    "ら": "ra",
    "り": "ri",
    "る": "ru",
    "れ": "re",
    "ろ": "ro",
    "わ": "wa",
    "を": "wo",
    "ん": "n"
}

romaji_to_hiragana = {
    "a": "あ",
    "i": "い",
    "u": "う",
    "e": "え",
    "o": "お",
    "ka": "か",
    "ki": "き",
    "ku": "く",
    "ke": "け",
    "ko": "こ",
    "sa": "さ",
    "shi": "し",
    "su": "す",
    "se": "せ",
    "so": "そ",
    "ta": "た",
    "chi": "ち",
    "tsu": "つ",
    "te": "て",
    "to": "と",
    "na": "な",
    "ni": "に",
    "nu": "ぬ",
    "ne": "ね",
    "no": "の",
    "ha": "は",
    "hi": "ひ",
    "fu": "ふ",
    "he": "へ",
    "ho": "ほ",
    "ma": "ま",
    "mi": "み",
    "mu": "む",
    "me": "め",
    "mo": "も",
    "ya": "や",
    "yu": "ゆ",
    "yo": "よ",
    "ra": "ら",
    "ri": "り",
    "ru": "る",
    "re": "れ",
    "ro": "ろ",
    "wa": "わ",
    "wo": "を",
    "n": "ん"
}

key = random.choice(list(hiragana_to_romaji.keys()))
hexo.japanese_value = hiragana_to_romaji[key]

async def send_message(value,good = None):
    text = ""
    if good != None:
        text = "Failed :(, the right answer was **"+good+"**. "
    text += "Try to guess **"+romaji_to_hiragana[value]+"**."
    welcome_id = hexo.client.get_channel(hexo.data["jap_channel_id"])
    await welcome_id.send(content = text)
    
async def new_message(message):
    
    if message.channel.id != hexo.data["jap_channel_id"]:
        return
    
    good = True

    if str(message.content).lower() == str(hexo.japanese_value).lower():
        await message.add_reaction("✅")
    else:
        await message.add_reaction("❌")
        good = False
        
    last = hexo.japanese_value
        
    key = random.choice(list(hiragana_to_romaji.keys()))
    hexo.japanese_value = hiragana_to_romaji[key]
        
    if good:
        await send_message(hexo.japanese_value)
    else:
        await send_message(hexo.japanese_value,last)
        
functions = {"on_message":new_message}
    