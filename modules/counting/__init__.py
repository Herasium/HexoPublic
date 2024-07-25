from __main__ import hexo
import discord
from mpmath import mp
from sympy import prime
import random

meta = {
    "name": "Counting Module",
    "id": "hera_counting",
    "ver": "0.0.1",
    "desc": "Used for the counting minigame.",
    "required": [],
    "author":"Herasium"
}

def int_to_bin(n):
    return bin(n)[2:]

def bin_to_int(b):
    return int(b, 2)

def roman_to_int(s):
    rom_val = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    int_val = 0
    for i in range(len(s)):
        if i > 0 and rom_val[s[i]] > rom_val[s[i - 1]]:
            int_val += rom_val[s[i]] - 2 * rom_val[s[i - 1]]
        else:
            int_val += rom_val[s[i]]
    return int_val

def int_to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
        ]
    syb = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
        ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syb[i]
            num -= val[i]
        i += 1
    return roman_num

def fibonacci_number(n):
    if n <= 0:
        return 0
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    
    a, b = 0, 1
    for _ in range(2, n):
        a, b = b, a + b
    
    return b

def number_to_letters(n):
    result = []
    while n > 0:
        n -= 1
        result.append(chr(n % 26 + ord('a')))
        n //= 26
    return ''.join(result[::-1])

def nth_digit_of_pi(n):
    mp.dps = n + 10
    pi_str = str(mp.pi).replace('.', '')
    return pi_str[n-1]

def nth_odd_number(n):
    return 2 * n - 1

def nth_even_number(n):
    return 2 * (n - 1)

def power_of_2(n):
    return 2 ** n

def nth_prime_number(n):
    return prime(n)

failed_reasons = [
    "Wrong Number (#1)",
    "You can't count twice in a row (#2)",
    "Unknown Error (#3)",
    "Invalid Mode Error (#4)",
    "Value Error (#5)",
]

new_modes_text = [
    ["Normal Counting","You count as normal, starting at 1 then 2,3,4..."],
    ["Binary Counting","You count as binary, starting at 1 then 10,11,100..."],
    ["Roman Counting","You count as roman numerals, starting at I then II,III,IV..."],
    ["Fibonacci Counting","You count as the fibonacci sequence, starting at 1 then 2,3,5,8..."],
    ["Hex Counting","You count as hex numbers, so base 16, starting at 0 then 1,2..,9,a,b..."],
    ["Pi Counting","You count as digits of pi, starting at 3 then 1,4,1..."],
    ["Odd Counting","You count as odd numbers, starting at 1 then 3,5,7..."],
    ["Even Counting","You count as even numbers, starting at 0 then 2,4,8..."],
    ["2^^ Counting","You count as powers of 2, starting at 2 then 4,8,16... (2^^n)"],
    ["Prime Counting","You count as prime numbers, starting at 2 then 3,5,7..."],
]

async def failed_counting_message(count,expected,user,reason):

    embed=discord.Embed(title="Wrong ❌", description=f"{user.name} has failed at {count+1}({expected})")
    embed.set_footer(text=failed_reasons[reason])

    counting_channel = hexo.client.get_channel(hexo.data["counting_channel_id"])

    await counting_channel.send(embed=embed)



async def new_mode():
    new_mode = random.randint(1,10)
    hexo.db.reference("/counting/mode").set(new_mode)
    hexo.db.reference("/counting/current").set(0)
    hexo.db.reference("/counting/last_id").set(0)   

    embed=discord.Embed(title=f"New Mode: {new_modes_text[new_mode-1][0]}", description=new_modes_text[new_mode-1][1])

    counting_channel = hexo.client.get_channel(hexo.data["counting_channel_id"])
    await counting_channel.send(embed=embed)

async def failed(count,expected,user,reason):
    await failed_counting_message(count,expected,user,reason)
    await new_mode()

async def new_counting_message(message):

    if message.channel.id != hexo.data["counting_channel_id"]:
        return

    num_ref = hexo.db.reference("/counting/current")
    mod_ref = hexo.db.reference("/counting/mode")
    last_ref = hexo.db.reference("/counting/last_id")

    current = num_ref.get()
    mode = mod_ref.get()
    last_user = last_ref.get()

    if last_user == message.author.id:
        await failed(current+1,"???",message.author,1)
        return  

    try:
        if mode == 1:
            expected = current + 1
        elif mode == 2:
            expected = int_to_bin(int(current + 1))
        elif mode == 3:
            expected = int_to_roman(current + 1)
        elif mode == 4:
            expected = f'{(current+1):x}'
        elif mode == 5:
            expected = fibonacci_number(current + 1)
        elif mode == 6:
            expected = int(nth_digit_of_pi(current + 1))
        elif mode == 7:
            expected = nth_odd_number(current + 1)
        elif mode == 8:
            expected = nth_even_number(current + 1)
        elif mode == 9:
            expected = power_of_2(current + 1)
        elif mode == 10:
            expected = nth_prime_number(current + 1)
        else:
            await failed(current+1,"???",message.author,3)
            return  # Invalid Mode Error
        

        if str(message.content).lower() == str(expected).lower():
            await message.add_reaction("✅")
            num_ref.set(current + 1)
            last_ref.set(message.author.id)
        else:
            await message.add_reaction("❌")
            await failed(current+1,expected,message.author,0)

    except ValueError as e:
        print(f"ValueError: {e}")
        await failed(current+1,"???",message.author,4)
        return
    except Exception as e:
        print(f"Error: {e}")
        await failed(current+1,"???",message.author,2)
        return

functions = {
    "on_message":new_counting_message
}