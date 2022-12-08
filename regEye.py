import discord
from discord.ext import commands
from discord.utils import get
import os
import requests, json
from bs4 import BeautifulSoup
import asyncio
from dotenv import load_dotenv

BOT_NAME = "RegEye"
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot_channel = 1050476403663048724
rcr = 738635228066611292
sendChannel = bot.get_channel(bot_channel)
rcrChannel = bot.get_channel(rcr)
botId = 1050457218295791616

i = 0



async def get_channel(playerName, name):
    global i
    sendChannel = bot.get_channel(bot_channel)
    check = await sendChannel.fetch_message(sendChannel.last_message_id)
    try:
        if (check.author.id == botId):
            return
        else:
            sendChannel = bot.get_channel(bot_channel)
            rcrChannel = bot.get_channel(rcr)
            channel = discord.utils.get(rcrChannel.guild.channels, name=playerName)
            # print(channel.id)
            await message_count(channel, name)
            i = 10000
    except AttributeError:
        pass


@bot.command()
async def message_count(channelId, name):
    sendChannel = bot.get_channel(bot_channel)
    channel = bot.get_channel(channelId)
    refId = channelId.id
    print(channelId)
    count = 0
    async for _ in channelId.history(limit=None):
        count += 1
    await sendChannel.send(f'There were {count} entries in the registry for {name}. (Reference: Channel ID {refId})')





@bot.command(name='report')
async def playerCheck(ctx, playerName):
    global i
    sendChannel = bot.get_channel(bot_channel)
    username = playerName
    userList = f'https://api.roblox.com/users/get-by-username?username={username}'

    headers = {
        "accept": "application/json"
    }

    response = requests.get(userList, headers=headers)
    data = response.json()

    userId = data['Id']
    # print(json.dumps(data, indent=2))
    print(userId)

    usernameHistory = f'https://users.roblox.com/v1/users/{userId}/username-history?limit=100&sortOrder=Asc'
    response = requests.get(usernameHistory, headers=headers)
    data2 = response.json()

    # print(json.dumps(data2, indent=2))
    length = len(data2['data'])
    print(length)
    i = 0
    names = []
    while (i < length):
        names.append(data2['data'][i]['name'])
        i += 1
    print(names)
    namesLength = len(names)
    i = 0
    skip = []
    while (i < namesLength):
        await asyncio.sleep(0.1)
        if names[i] in skip:
            i += 1
        elif names[i] not in skip:
            lowerName = (names[i].lower())
            await get_channel(lowerName, playerName)
            skip.append(names[i])
            print(names[i])
            i += 1


    # sendChannel.send(names)

bot.run(DISCORD_TOKEN)
