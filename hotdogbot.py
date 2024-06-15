# hotdogbot.py
import os
import json
from pathlib import Path
import random
import re
import math
import time

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.all())

n_word_usages = {}
n_word_file_path = Path("n_words.json")
if n_word_file_path.is_file():
    with open(n_word_file_path, 'r') as f:
        n_word_usages = json.load(f)
n_word_regex_pattern = r'n+[i|1l]+[g6]+[e3]+[r2]+'
n_word_regex = re.compile(n_word_regex_pattern)

sticker_bans_file_path = Path("sticker_bans.json")
if sticker_bans_file_path.is_file():
    with open(sticker_bans_file_path, 'r') as f:
        sticker_bans = json.load(f)

house_cup_points = {
    "Gryffindor": [],
    "Slytherin": [],
    "Ravenclaw": [],
    "Hufflepuff": []
}

house_rank_ids = {
    1041031924409450496: "Gryffindor",
    1041032027404775485: "Slytherin",
    1041032103120351333: "Ravenclaw",
    1041032073567277156: "Hufflepuff"
}

house_cup_points_file_path = Path("house_cup.json")
if house_cup_points_file_path.is_file():
    with open(house_cup_points_file_path, 'r') as f:
        house_cup_points = json.load(f)

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

balls_regex_pattern = r'https://cdn.discordapp.com/attachments/[0-9]+/[0-9]+/wall.gif'
balls_regex_pattern2 = r'https://media.discordapp.net/attachments/[0-9]+/[0-9]+/wall.gif'
balls_regex = re.compile(balls_regex_pattern)
balls_regex2 = re.compile(balls_regex_pattern2)

banned_users = [631068575406358539]

@client.event
async def on_message(message):
    if message.author == client.user or message.author.bot or message.author.id in banned_users:
        return

    if message.guild.id == 1083466447164018738:
        if balls_regex.search(message.content.lower()) or balls_regex2.search(message.content.lower()):
            await message.channel.send("ball shitters O U T")
            await message.delete()

    if message.stickers:
        sticker = await message.stickers[0].fetch()
        if str(message.guild.id) in sticker_bans and sticker.id in sticker_bans[str(message.guild.id)]["bans"]:
            await message.channel.send("degen stickers O U T")
            await message.delete()
        elif str(message.guild.id) in sticker_bans and sticker.guild_id in sticker_bans[str(message.guild.id)]["serverbans"]:
            await message.channel.send("degen stickers O U T")
            await message.delete()

    if message.content.lower() == ",r stickerban" and message.author.id == 200019140105207808:
        msg = await message.channel.fetch_message(message.reference.message_id)
        sticker = await msg.stickers[0].fetch()
        if str(message.guild.id) in sticker_bans:
            sticker_bans[str(message.guild.id)]["bans"].append(sticker.id)
        else:
            sticker_bans[str(message.guild.id)] = {
                "bans": [sticker.id],
                "serverbans": []
            }
        with open(sticker_bans_file_path, 'w', encoding='utf-8') as f:
            json.dump(sticker_bans, f, ensure_ascii=False, indent=4)
        await msg.delete()
        await message.channel.send("b&")

    if message.content.lower() == ",r stickerserverban" and message.author.id == 200019140105207808:
        msg = await message.channel.fetch_message(message.reference.message_id)
        sticker = await msg.stickers[0].fetch()
        if str(message.guild.id) in sticker_bans:
            sticker_bans[str(message.guild.id)]["serverbans"].append(sticker.guild_id)
        else:
            sticker_bans[str(message.guild.id)] = {
                "bans": [],
                "serverbans": [sticker.guild_id]
            }
        with open(sticker_bans_file_path, 'w', encoding='utf-8') as f:
            json.dump(sticker_bans, f, ensure_ascii=False, indent=4)
        await msg.delete()
        await message.channel.send("server b&")

    if message.content.lower() == ',r hotdog':
        response = "https://i.redd.it/w5as70kigbw61.jpg"
        await message.channel.send(response)

    if message.content.lower() == ',r longdog':
        response = "https://media.discordapp.net/attachments/1083466447734452308/1224499186033102868/magik.png?ex=661db6bc&is=660b41bc&hm=50cceaa084117cdb26356511b3f7b86d40c3c0f8fbe4b0a7d9290185517f5638&=&format=webp&quality=lossless"
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
                all_usages = [m.start() for m in re.finditer(n_word_regex_pattern, usage['content'].replace(" ", "").replace("\n", "").replace("\t", ""))]
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

    if message.author.id == 666822401232863242:
        msg = message.content.lower()
        if 'based' in msg and 'cringe' in msg and '14' in msg and '88' in msg:
            await message.reply("shut up you inbred monkey")
            return

    if 'based' in message.content.lower():
        await message.reply(f"{random.randint(0, 100),:.2f}% based")
        
    if 'cringe' in message.content.lower():
        await message.reply(f"{random.randint(0, 100):.2f}% cringe")

    # grab retard role id
    role = message.guild.get_role(917583501526724638)
    role2 = message.guild.get_role(1042140848449650769)
    if role in message.author.roles or role2 in message.author.roles:
        # if author is a confirmed retard, roll .1 chance jingles will remind him
        if math.floor(random.random()*1001) == 1:
            await message.channel.send(f"<@{message.author.id}> jingles says you're a fucking retard", file=discord.File('./assets/jingles.jpg'))

    if math.floor(random.random()*100000) == 1:
        await message.channel.send(f"<@{message.author.id}>, you have been visited by the golden jingles, this jingles only appears once in every 100,000 messages.", file=discord.File('./assets/goldjingles.png'))

    if math.floor(random.random()*1000000) == 1:
        await message.channel.send(f"<@{message.author.id}>, you have been visited by the mythical jingles, this jingles only appears once in every 1,000,000 messages. @everyone rejoice", file=discord.File('./assets/mythicaljingles.png'))

    if message.channel.name == "cleared-cleared-cleared":
        if len(message.attachments) > 0:
            await message.add_reaction("✅")
            await message.add_reaction("❌")
        elif not message.guild.get_role(697270930312790017) in message.author.roles or not message.guild.get_role(936910296558211134) in message.author.roles:
            await message.delete()

    if message.content.lower().startswith(",hcaward") and message.guild.id == 1041009215059271750 and message.author.id == 300270511559278592:
        mentioned_users = message.mentions
        if len(mentioned_users) == 1:
            mentioned_user = mentioned_users[0]
            user_house = []
            for role in mentioned_user.roles:
                if role.id in house_rank_ids:
                    user_house.append(house_rank_ids[role.id])
            if len(user_house) == 0:
                await message.channel.send("Failed: Mentioned user " + mentioned_user.display_name + " has no house ranks.")
            elif len(user_house) > 1:
                await message.channel.send("Failed: Mentioned user " + mentioned_user.display_name + " has multiple house ranks.")
            else:
                _, awarded_user, point_value, reason = message.content.split(" ", 3)
                point_value = float(point_value)
                if awarded_user and point_value and reason:
                    if point_value == 0:
                        await message.channel.send("Failed: You must award a nonzero amount of points")
                    else:
                        award = {
                            "awarded_user": awarded_user,
                            "point_value": point_value,
                            "reason": reason,
                            "time": message.created_at.strftime("%H:%M:%S UTC, on %m/%d/%Y")
                        }
                        house_cup_points[user_house[0]].append(award)
                        with open(house_cup_points_file_path, 'w', encoding='utf-8') as f:
                            json.dump(house_cup_points, f, ensure_ascii=False, indent=4)
                        if point_value > 0:
                            await message.channel.send("Awarded " + str(point_value) + " points to " + mentioned_user.display_name + " of House " + user_house[0] + " for:\n" + reason)
                        else:
                            await message.channel.send("Subtracted " + str(point_value) + " points from " + mentioned_user.display_name + " of House " + user_house[0] + " for:\n" + reason)
                else:
                    await message.channel.send("Failed: usage is ',hcaward <mention someone here> <point value, nonzero integer> <reason>")
        else:
            await message.channel.send("Failed: You must only mention exactly one user in ,hcaward because the discord API is gay and doesn't order the mentions in a message if there are multiple.")

    if message.content.lower().startswith(",hcranks") and message.guild.id == 1041009215059271750:
        house_strings = {
            "Gryffindor": "GRYFFINDOR: ",
            "Slytherin": "SLYTHERIN: ",
            "Ravenclaw": "RAVENCLAW: ",
            "Hufflepuff": "HUFFLEPLUFF: "
        }
        for house in house_cup_points:
            counter = 1
            temp_string = ""
            point_total = 0.0
            for award in house_cup_points[house]:
                point_total += float(award["point_value"])
                if float(award["point_value"]) > 0:
                    temp_string += str(counter) + ". Awarded " + str(award["point_value"]) + " points to " + award["awarded_user"] + " for: " + award["reason"] + " (time: " + award["time"] + ")\n"
                else:
                    temp_string += str(counter) + ". Subtracted " + str(award["point_value"]) + " points from " + award["awarded_user"] + " for: " + award["reason"] + " (time: " + award["time"] + ")\n"
                counter += 1
            house_strings[house] += str(point_total) + " total points\n" + temp_string
        await message.channel.send("HOUSE CUP RANKINGS:")
        for house_string in house_strings:
            await message.channel.send(house_strings[house_string], allowed_mentions=discord.AllowedMentions.none())

    # a votekick is initiated
    if message.content.lower()[0:11] == ',r votekick':
        # the og users is vote number 1
        count = 1
        messageArr = message.content.split()
        # if they forgot a username
        if len(messageArr) < 3:
            await message.channel.send("You forgot to say who to kick you fucking idiot.")
        else:
            user = message.content.split()[2]
            # begin votekick countdown
            await message.channel.send("A votekick countdown has begun for: " + user + ". Type ,votekick to vote.", allowed_mentions=discord.AllowedMentions.none())
            time.sleep(15)
            # register initiator in table
            kickTable = [message.author.name]
            # iterate over all msgs in last 30 secs
            async for msg in message.channel.history(after = message.created_at):
                # if msg starts with ,votekick
                if msg.content[0:9] == ",votekick":
                    # people can only vote once
                    if msg.author.name not in kickTable:
                        count+=1
                        kickTable.append(msg.author.name)
            # output results of vote
            await message.channel.send("Kicked user " + user + " with " + str(count) + " votes! ", allowed_mentions=discord.AllowedMentions.none())
            
client.run(TOKEN)
