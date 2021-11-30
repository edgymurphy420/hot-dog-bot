# hotdogbot.py
import os
import json
from pathlib import Path
import random
import re

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

n_word_usages = {}
n_word_file_path = Path("n_words.json")
if n_word_file_path.is_file():
    with open(n_word_file_path, 'r') as f:
        n_word_usages = json.load(f)
n_word_regex_pattern = r'n+[i|1l]+[g6]+[e3]+[r2]+'
n_word_regex = re.compile(n_word_regex_pattern)

eight_ball_responses = [
    "It is certain, ",
    "Yes, ",
    "Most likely, ",
    "you're question is cringe, kys ",
    "ur a retard ",
    "Don't count on it, ",
    "No, ",
    "Not a chance, ",
    "ok, ",
    "what "
]

src_messages = [
    ",r src",
    ",r source",
    ",r sourcecode",
    ",r source code"
]

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot:
        return

    if message.content.lower() == ',r hotdog':
        response = "https://i.redd.it/w5as70kigbw61.jpg"
        await message.channel.send(response)

    if message.content.lower() in src_messages:
        response = "https://github.com/edgymurphy420/hot-dog-bot"
        await message.channel.send(response)

    if n_word_regex.search(message.content.lower().replace(" ", "").replace("\n", "").replace("\t", "")):
        usage = {
            "author": message.author.mention,
            "content": message.content,
            "time": message.created_at.strftime("%H:%M:%S UTC, on %m/%d/%Y"),
            "server": message.guild.name
        }
        if str(message.guild.id) in n_word_usages:
            n_word_usages[str(message.guild.id)].append(usage)
        else:
            n_word_usages[str(message.guild.id)] = [usage]
        with open(n_word_file_path, 'w', encoding='utf-8') as f:
            json.dump(n_word_usages, f, ensure_ascii=False, indent=4)

    if message.content.lower() == ',r nword':
        if str(message.guild.id) in n_word_usages:
            usage = random.choice(n_word_usages[str(message.guild.id)])
            if len(usage['content']) >= 200:
                all_usages = [m.start() for m in re.finditer(n_word_regex_pattern, usage['content'])]
                first_usage_index = all_usages[0]
                start_index = first_usage_index - 100 if first_usage_index - 100 > 0 else 0
                end_index = first_usage_index + 100 if first_usage_index + 100 < len(usage['content']) else len(usage['content'])
                shortened_usage = usage['content'][start_index:end_index]
                response = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:\n[...]{shortened_usage}[...]".replace("\n", "\n> ")
            else:
                response = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:\n{usage['content']}".replace("\n", "\n> ")
            await message.channel.send(response, allowed_mentions=discord.AllowedMentions.none())
        else:
            response = "Nobody has used the N word in this server since I had this feature added. hotdogbot is proud of you all."
            await message.channel.send(response)

    if len(message.content.lower()) >= 8 and message.content.lower()[0:8] == ",r 8ball":
        response = random.choice(eight_ball_responses) + str(message.author.name)
        await message.channel.send(response)
        return

    if 'based' in message.content.lower():
        await message.channel.send(f"{random.randint(0, 100)}% based")
        
    if 'cringe' in message.content.lower():
        await message.channel.send(f"{random.randint(0, 100)}% cringe")


client.run(TOKEN)
