import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from toolz.dicttoolz import get_in

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

from craft_interface import *
from data.itemdb import get_itemdb
from data.inventory_display import create_inventory_image

@bot.command(name='inventory', help='retrieves the inventory of an ethercraft character')
async def get_inventory_entrypoint(ctx, character_id: int):
    inventory = get_inventory(character_id)
    upload_file = create_inventory_image(inventory)
    # itemdb = get_itemdb()
    # upload_files = []

    # for item in inventory.items:
    #     png_path = itemdb[item].get('png_path')
    #     if png_path:
    #         upload_files.append(discord.File(png_path))

    await ctx.send(file=discord.File(upload_file))

@bot.command(name='equipment', help='retrieves the equipment of an ethercraft character')
async def get_equipment_entrypoint(ctx, character_id: int):
    await ctx.send(get_equipment(character_id))

@bot.event
async def on_ready():
    initialise_itemdb()
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if "bot" in message.content:
        response = "<:feelshekman:588164589238091802>"
        await message.channel.send(response)

    await bot.process_commands(message)

bot.run(TOKEN)