# hotdogbot.py
import os
import json
from pathlib import Path
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

n_word_usages = []
n_word_file_path = Path("n_words.json")
if n_word_file_path.is_file():
    with open(n_word_file_path, 'r') as f:
        n_word_usages = json.load(f)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == ',r hotdog':
        response = "https://i.redd.it/w5as70kigbw61.jpg"
        await message.channel.send(response)

    if message.content.lower() == ',r nword':
        if n_word_usages:
            usage = random.choice(n_word_usages)
            response = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:\n> {usage['content']}"
        else:
            response = "Nobody has used the N word in this server since I had this feature added. hotdogbot is proud of you all."
        await message.channel.send(response)

    if "nigger" in message.content.lower():
        usage = {
            "author": message.author.mention,
            "content": message.content,
            "time": message.created_at.strftime("%H:%M:%S UTC, on %m/%d/%Y"),
            "server": message.guild.name
        }
        n_word_usages.append(usage)
        with open(n_word_file_path, 'w', encoding='utf-8') as f:
            json.dump(n_word_usages, f, ensure_ascii=False, indent=4)


client.run(TOKEN)