import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import View, Button, Select
import os
import random
from dotenv import load_dotenv
import asyncio

load_dotenv()

token = os.getenv('TOKEN')
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=["!", "?"], intents=intents)

COUNTING_CHANNEL = 1504485545479504103
snumber = random.randint(1, 100)
fromstart = 1
lastUser = ""

class Math(discord.ui.Select):
    def __init__(self, answer):
        self.answer = round(answer, 2)
        options = [discord.SelectOption(label=str(self.answer), description="Is this the answer?")]
        
        while len(options) < 3:
            wrong_ans = round(self.answer + random.choice([-1, 1]) * random.randint(1, 100), 2)
            if str(wrong_ans) not in [opt.label for opt in options]:
                options.append(discord.SelectOption(label=str(wrong_ans), description="Is this the answer?"))
                
        random.shuffle(options)
        
        super().__init__(
            placeholder="Choose the correct answer...",
            min_values=1,
            max_values=1,
            options=options
        )
        
    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == str(self.answer):
            await interaction.response.send_message("Correct! 🎉")
        else:
            await interaction.response.send_message(f"Wrong! The correct answer was {self.answer} ❌")

class Mathview(View):
    def __init__(self, answer):
        super().__init__()
        self.add_item(Math(answer))

class RPSFriendDropdown(discord.ui.Select):
    def __init__(self, game_view, player_type):
        self.game_view = game_view
        self.player_type = player_type
        options = [
            discord.SelectOption(label="Rock", emoji="🪨"),
            discord.SelectOption(label="Paper", emoji="📄"),
            discord.SelectOption(label="Scissor", emoji="✂️")
        ]
        super().__init__(placeholder="Choose your move...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        if self.player_type == 'host' and interaction.user != self.game_view.host:
            return await interaction.response.send_message("This dropdown is not for you!", ephemeral=True)
        if self.player_type == 'guest' and interaction.user != self.game_view.guest:
            return await interaction.response.send_message("This dropdown is not for you!", ephemeral=True)

        if self.player_type == 'host':
            self.game_view.host_choice = self.values[0]
        else:
            self.game_view.guest_choice = self.values[0]

        await interaction.response.send_message(f"You selected {self.values[0]}!", ephemeral=True)
        
        await self.game_view.check_results()

class RPSGameView(View):
    def __init__(self, host, guest, channel):
        super().__init__(timeout=60)
        self.host = host
        self.guest = guest
        self.channel = channel
        self.host_choice = None
        self.guest_choice = None

    async def check_results(self):
        if self.host_choice and self.guest_choice:
            self.stop()
            
            h_choice = self.host_choice
            g_choice = self.guest_choice
            
            if h_choice == g_choice:
                result_text = f"It's a tie! Both chose **{h_choice}**"
            elif (h_choice == "Rock" and g_choice == "Scissor") or \
                 (h_choice == "Paper" and g_choice == "Rock") or \
                 (h_choice == "Scissor" and g_choice == "Paper"):
                result_text = f"🏆 **{self.host.name}** wins! (**{h_choice}** beats **{g_choice}**)"
            else:
                result_text = f"🏆 **{self.guest.name}** wins! (**{g_choice}** beats **{h_choice}**)"

            await self.channel.send(f"🎮 **RPS Match Results between {self.host.mention} and {self.guest.mention}:**\n{result_text}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user.name} and synced slash commands!")

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
                    lastUser = ""
                    await message.add_reaction("❌")
                    await message.channel.send(f"<@{message.author.id}> did it wrong! Next number: 1")
            else:
                fromstart = 1
                lastUser = ""
                await message.channel.send(f"<@{message.author.id}> typed something that isn't a number! Next number: 1")
        else:
            fromstart = 1
            lastUser = ""
            await message.channel.send(f"<@{message.author.id}>! Wait for someone else to play! Next number: 1")

@bot.tree.command(name="guessn", description="Guess the number")
async def guessn(interaction: discord.Interaction, number: int):
    global snumber
    if number == snumber:
        await interaction.response.send_message(f"🎉 You caught the number! The number was: {snumber}")
        snumber = random.randint(1, 100)
    elif number > snumber:
        await interaction.response.send_message("The secret number is lower 🔽")
    elif number < snumber:
        await interaction.response.send_message("The secret number is higher 🔼")

@bot.tree.command(name="math", description="Answer a math question")
async def math(interaction: discord.Interaction):
    first = random.randint(1, 100)
    second = random.randint(1, 100)
    operation = random.choice(["+", "-", "*"])
    
    if operation == "+":
        answer = first + second
    elif operation == "-":
        answer = first - second
    elif operation == "*":
        answer = first * second

    await interaction.response.send_message(f"What is **{first} {operation} {second}**?", view=Mathview(answer))

@bot.tree.command(name="rps", description="Play rock paper scissors against the bot")
async def rps(interaction: discord.Interaction, choice: str):
    choices = choice.lower()
    items = ["rock", "paper", "scissor"]
    if choices not in items:
        return await interaction.response.send_message("Invalid choice! Choose rock, paper, or scissor.", ephemeral=True)
        
    b_choice = random.choice(items)
    if choices == b_choice:
        await interaction.response.send_message(f"It's a tie! Both chose **{choices}**")
    elif (choices == "rock" and b_choice == "scissor") or \
         (choices == "paper" and b_choice == "rock") or \
         (choices == "scissor" and b_choice == "paper"):
        await interaction.response.send_message(f"You win! 🎉 You chose **{choices}** and the bot chose **{b_choice}**")
    else:
        await interaction.response.send_message(f"You lose! 😢 You chose **{choices}** and the bot chose **{b_choice}**")

@bot.tree.command(name="rpswithfriend", description="Play rock paper scissors with a friend")
async def rpswithfriend(interaction: discord.Interaction, friend: discord.Member):
    if friend == interaction.user:
        return await interaction.response.send_message("You can't play against yourself!", ephemeral=True)
    if friend.bot:
        return await interaction.response.send_message("You can't play against a bot here! Use `/rps` instead.", ephemeral=True)

    await interaction.response.send_message(f"⚔️ {interaction.user.mention} challenged {friend.mention} to Rock Paper Scissors! Check your Direct Messages!")

    game_view = RPSGameView(host=interaction.user, guest=friend, channel=interaction.channel)

    host_view = View()
    host_view.add_item(RPSFriendDropdown(game_view, 'host'))
    
    guest_view = View()
    guest_view.add_item(RPSFriendDropdown(game_view, 'guest'))

    try:
        await interaction.user.send(f"You challenged {friend.name}! Choose your move below:", view=host_view)
        await friend.send(f"{interaction.user.name} challenged you to RPS! Choose your move below:", view=guest_view)
    except discord.Forbidden:
        await interaction.channel.send("Could not send a DM to one of the players. Make sure your DMs are open!")

bot.run(token)
