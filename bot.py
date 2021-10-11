import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

from craft_interface import *

@bot.command(name='inventory', help='retrieves the inventory of an ethercraft character')
async def get_inventory_entrypoint(ctx, character_id: int):
    await ctx.send(get_inventory(character_id))

@bot.command(name='equipment', help='retrieves the equipment of an ethercraft character')
async def get_equipment_entrypoint(ctx, character_id: int):
    await ctx.send(get_equipment(character_id))

@bot.event
async def on_ready():
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