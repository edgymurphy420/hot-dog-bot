# hotdogbot.py
import os

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower() == ',r hotdog':
        response = "https://i.redd.it/w5as70kigbw61.jpg"
        await message.channel.send(response)

client.run(TOKEN)