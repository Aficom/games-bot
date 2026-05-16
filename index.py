import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button
import os
import random
from dotenv import load_dotenv
load_dotenv()
from keep_alive import keep_alive
import asyncio
token = os.getenv('TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["!", "?"], intents=intents)
COUNTING_CHANNEL = 1504485545479504103
snumber = random.randint(1, 100)
fromstart = 1
lastUser = ""
first = 0
second = 0
@bot.event
async def on_ready():
    synched = await bot.tree.sync()
    try:
        if len(synched) == 0:
            return print("No command found")
        print(f"Successfully loaded {len(synched)}")
        print(f"Logged in as {bot.user.name}")
    except Exception as e:
        print(f"Something went wrong! Error : {e}")

@bot.event
async def on_message(message):
    global lastUser, fromstart
    if message.author == bot.user:
        return
    if message.channel.id == COUNTING_CHANNEL:
        if str(message.author.id) != lastUser:
            if message.content.isdigit():
                if int(message.content) == fromstart:
                    lastUser = str(message.author.id)
                    fromstart += 1
                    await message.add_reaction("✅")
                else:
                    fromstart = 1
                    await message.add_reaction("❌")
                    await message.channel.send(f"<@{message.author.id}> did it wrong! Next number: 1")
            else:
                fromstart = 1
                await message.channel.send(f"<@{message.author.id}> did it wrong! Next number: 1")
        else:
            fromstart = 1
            await message.channel.send(f"<@{message.author.id}> ! Wait for someone else to play! Next number: 1")
@bot.tree.command(name="guessn", description="Guess the number")
async def guessn(interaction:discord.Interaction, number:int):
    global snumber
    if number == snumber:
        await interaction.response.send_message(f"You catched the number! The number was: {snumber}")
        snumber = random.randint(1, 100)
    elif number > snumber:
        await interaction.response.send_message("The secret number is less than that number")
    elif number < snumber:
        await interaction.response.send_message("The secret number is greater than that number")
    
keep_alive()
bot.run(token)
