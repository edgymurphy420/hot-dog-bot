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

n_word_usages = []
n_word_file_path = Path("n_words.json")
if n_word_file_path.is_file():
    with open(n_word_file_path, 'r') as f:
        n_word_usages = json.load(f)
n_word_regex_pattern = r'[n\s]+[i|1l\s]+[g6\s]+[e3\s]+[r2\s]+'
n_word_regex = re.compile(n_word_regex_pattern)

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
            if len(usage['content']) >= 200:
                all_usages = [m.start() for m in re.finditer(n_word_regex_pattern, usage['content'])]
                first_usage_index = all_usages[0]
                start_index = first_usage_index - 100 if first_usage_index - 100 > 0 else 0
                end_index = first_usage_index + 100 if first_usage_index + 100 < len(usage['content']) else len(usage['content'])
                shortened_usage = usage['content'][start_index:end_index]
                response = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:\n[...]{shortened_usage}[...]".replace("\n", "\n> ")
            else:
                response = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:\n{usage['content']}".replace("\n", "\n> ")
            await message.channel.send(response)
            """
            if len(usage['content']) >= 3996:
                response1 = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:"
                await message.channel.send(response1)
                response2 = f"> {usage['content'][:1998]}"
                await message.channel.send(response2)
                response3 = f"> {usage['content'][1998:3996]}"
                await message.channel.send(response3)
                response4 = f"> {usage['content'][3996:]}"
                await message.channel.send(response4)
            elif len(usage['content']) >= 1998:
                response1 = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:"
                await message.channel.send(response1)
                response2 = f"> {usage['content'][:1998]}"
                await message.channel.send(response2)
                response3 = f"> {usage['content'][1998:]}"
                await message.channel.send(response3)
            elif len(usage['content']) >= 1850:
                response1 = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:"
                await message.channel.send(response1)
                response2 = f"> {usage['content']}"
                await message.channel.send(response2)
            else:
                response = f"At {usage['time']}, {usage['author']} said this in {usage['server']}:\n{usage['content']}"
                await message.channel.send(response)
                """
        else:
            response = "Nobody has used the N word in this server since I had this feature added. hotdogbot is proud of you all."
            await message.channel.send(response)

    if n_word_regex.search(message.content.lower().replace(" ", "")):
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