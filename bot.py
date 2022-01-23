import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from toolz.dicttoolz import get_in
from time import sleep

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

from tools.craft_interface import BotInterface
from tools.inventory_display import InventoryRenderer
from data.events.parser import parse_events

iface = BotInterface()
renderer = InventoryRenderer(iface.ec.items)

@bot.command(name='inventory', help='retrieves the inventory of an ethercraft character')
async def get_inventory_entrypoint(ctx, character_id: int):
    inventory = iface.get_inventory(character_id)
    upload_file = renderer.create_inventory_image(inventory)
    await ctx.send(file=discord.File(upload_file))

# @bot.command(name='runlog', help='lists the events of an ethercraft dungeon run')
# async def get_runlog_entrypoint(ctx, run_idx: int):
#     message = await ctx.send("collecting run data")
#     run_data = iface.get_run_info([run_idx])

#     message_content = ""

#     for log in parse_events(run_data):
#         message_content += f"{log}\n"
    
#     await ctx.send(message_content)

# @bot.command(name='run', help='lists the events of an ethercraft dungeon run')
# async def get_run_entrypoint(ctx, run_idx: int):
#     message = await ctx.send("collecting run data")
#     run_data = iface.get_run_info([run_idx])

#     for log in parse_events(run_data):
#         await message.edit(content=log)
#         sleep(3)

@bot.command(name='equipment', help='retrieves the equipment of an ethercraft character')
async def get_equipment_entrypoint(ctx, character_id: int):
    await ctx.send(iface.get_equipment(character_id))

@bot.event
async def on_ready():
    
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # if "bot" in message.content:
    #     response = "<:feelshekman:588164589238091802>"
    #     await message.channel.send(response)
    
    # if "busted" in message.content.lower():
    #     response = ":100:"
    #     await message.channel.send(response)

    await bot.process_commands(message)

bot.run(TOKEN)