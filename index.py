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
class Math(discord.ui.Select):
    def __init__(self, answer):
        options = []
        fst = random.choice(["first", "second", "third"])
        if fst == "first":
            options.append(discord.SelectOption(label=str(round(answer, 2)), description="The first number"))
            options.append(discord.SelectOption(label=str(round(answer+random.randint(1, 100), 2)), description="The second number"))
            options.append(discord.SelectOption(label=str(round(answer-random.randint(1, 100), 2)), description="The third number"))
        elif fst == "second":
            options.append(discord.SelectOption(label=str(round(answer+random.randint(1, 100), 2)), description="The first number"))
            options.append(discord.SelectOption(label=str(round(answer, 2)), description="The second number"))
            options.append(discord.SelectOption(label=str(round(answer-random.randint(1, 100), 2)), description="The third number"))
        elif fst == "third":
            options.append(discord.SelectOption(label=str(round(answer+random.randint(1, 100), 2)), description="The first number"))
            options.append(discord.SelectOption(label=str(round(answer-random.randint(1, 100), 2)), description="The second number"))
            options.append(discord.SelectOption(label=str(round(answer, 2)), description="The third number"))
        super().__init__(
            placeholder="Choose the correct answer...",
            min_values=1,
            max_values=1,
            options=options
        )
        
        self.answer = answer
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == str(round(self.answer, 2)):
            await interaction.response.send_message("Correct!")
        else:
            await interaction.response.send_message(f"Wrong! The correct answer was {round(self.answer, 2)}")
class Mathview(View):
    def __init__(self, answer):
        super().__init__()
        self.add_item(Math(answer))
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
@bot.tree.command(name="math", description="answer to a math question")
async def math(interaction:discord.Interaction):
    first = random.randint(1, 10000)
    second = random.randint(1, 10000)
    operation = random.choice(["+", "-", "*", "/"])
    answer = 0
    if operation == "+":
        answer = first + second
    elif operation == "-":
        answer = first - second
    elif operation == "*":
        answer = first * second
    elif operation == "/":
        answer = first / second
    await interaction.response.send_message(f"What is {first} {operation} {second}?", view=Mathview(answer))
keep_alive()
bot.run(token)
