import discord
from discord.ext import commands
from discord import app_commands
import os
import random
from dotenv import load_dotenv
load_dotenv()
from keep_alive import keep_alive
token = os.getenv('TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["!", "?"], intents=intents)
counting_channel = 1504485545479504103
tic_tac_toe_channel = 1504485545479504103
fruits = ["rocket", "spin", "blade", "spring", "bomb", "smoke", "spike", "flame", "dark", "sand", "ice", "rubber", "eagle", "ghost", "light", "diamond", "quake", "magma", "love", "spider", "sound", "phoenix", "creation", "blizzard", "buddha", "portal", "shadow", "venom", "spirit", "mammonth", "gravity", "trex", "dough", "gas", "lightning", "tiger", "yeti", "kitsune", "control", "dragon", "dragoneast", "dragonwest"]
start = 0
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(f'Error syncing commands: {e}')
@bot.event
async def on_message(message):
    global start
    if message.author.bot:
        return
    if message.channel.id == counting_channel:
        
        if message.content.isdigit():
            if int(message.content) == start + 1:
                start += 1
                await message.add_reaction('✅')
            else:
                start = 0
                await message.add_reaction('❌')
                await message.channel.send(f'{message.author.mention} Please count in order! The next number is {start + 1}.')   
@bot.tree.command(name="roll", description="Get a random fruit from the list")
async def roll(interaction: discord.Interaction):
    fruit = random.choice(fruits)
    await interaction.response.send_message(f'{interaction.user.mention} You rolled: {fruit}')

bot.run(token)
keep_alive()