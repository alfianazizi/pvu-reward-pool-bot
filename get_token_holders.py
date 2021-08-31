import asyncio
from bscscan import BscScan

import asyncio
import os
from itertools import cycle

import aiohttp
import discord
import random
from discord.ext import commands, tasks
from discord_slash import SlashCommand
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix=";")
slash = SlashCommand(client, sync_commands=True)

discord_token = os.environ['DISCORD_TOKEN']
bscscan_token = os.environ['BSC_TOKEN']
contract_address = os.environ['CONTRACT_ADDRESS']
holder_address = os.environ['HOLDER_ADDRESS']

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    task_update_activity.start()


async def value_of_currency_to_show():
    async with BscScan(bscscan_token) as bsc:
      return(int(float(await bsc.get_acc_balance_by_token_contract_address(contract_address=contract_address, address=holder_address))/10**18))


@tasks.loop(seconds=5.0)
async def task_update_activity():
    for guild in client.guilds:
        await guild.me.edit(nick=f"{(await value_of_currency_to_show()):,} PVU")
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="PVU Reward Pool"))

client.run(discord_token)
