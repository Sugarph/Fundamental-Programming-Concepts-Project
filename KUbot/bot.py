import os
import discord
from discord.ext import commands
from discord import Embed, Colour
from dotenv import load_dotenv
import time
from pymyku.utils import extract
import pymyku
from utils import *
import json


DAY_COLORS = {
    'MON': Colour.yellow(),
    'TUE': Colour.pink(),
    'WED': Colour.green(),
    'THU': Colour.orange(),
    'FRI': Colour.blue(),
    'SAT': Colour.purple(),
    'SUN': Colour.red()
}

intents = discord.Intents.all()
intents.message_content = True  # Allow access to message content

client = commands.Bot(command_prefix='!', intents=intents)
user_data = {}



@client.event
async def on_ready():
    print("KUbot is now online!")

@client.command()
async def ping(ctx):# Resond pong! with time it take in ms
    start_time = time.time()
    message = await ctx.send("Pong!")  
    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000
    await message.edit(content=f"Pong! Round-trip time: {duration_ms:.2f} ms")

@client.command()
async def join(ctx):
    if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
    else:
        await ctx.send("You are not in a voice channel.")

@client.command()
async def leave(ctx): 
    if ctx.voice_client and ctx.voice_client.guild == ctx.guild: # Check if the bot is in a voice channel in the same guild as the author
        channel_left = ctx.author.voice.channel
        await ctx.voice_client.disconnect()
        await ctx.send(f"I has left from {channel_left} channel")
    else:
        await ctx.send("I am not in a voice channel.")

@client.command()
async def next(ctx): 
    user_id = ctx.author.id
    if not await user_check(ctx, user_id):  
        return
    user_info = user_data[user_id]

    api_response = user_info["api_response"]
    upcoming_class, current_day = get_upcoming_class(api_response)

    #Create embed
    if upcoming_class:
        embed = discord.Embed(title="Next Class", description = upcoming_class['Subject'], color = DAY_COLORS[current_day])
        embed.add_field(name="Class start time", value=f"<t:{upcoming_class['UnixStartTime']}>", inline=False)
        embed.add_field(name="Time until class start", value=f"<t:{upcoming_class['UnixStartTime']}:R>", inline=False)
        embed.add_field(name="Room", value= upcoming_class['Room'], inline=False)
    else:
        embed = discord.Embed(title="No upcoming class today.", color = DAY_COLORS[current_day])

    # Send the embed
    await ctx.send(embed=embed)
    print("Next command called")
    

@client.command()
async def register(ctx):
    user = ctx.author
    await user.send("Please provide your username and password in the following format: Username:Password") #Send DMs to user 
    
    def check(msg):
        return msg.author == user and msg.channel.type == discord.ChannelType.private  #Check is message from dm is same user who call the command
    
    response_msg = await client.wait_for('message', check=check, timeout=300) 
    try:
        username, password = response_msg.content.split(':')
        ku_client = pymyku.Client(username, password)
        response = ku_client.fetch_group_course()
        api_call_time = time.time()
        user_data[user.id] = {
            "api_response": response,
            "last_api_call": api_call_time
        }
    except:
        await user.send("Something went wrong!")

    await user.send("Successfully registered!")
    print("register command called")

async def user_check(ctx, user_id):
    if user_id not in user_data:
        await ctx.send("You are not registered. Please use the !register command.")
        return 

    user_info = user_data[user_id]
    last_api_call = user_info.get("last_api_call", 0)
    current_time = time.time()

    if current_time - last_api_call >= 86400:
        await ctx.send("It's been more than 1 day since the last data update. Please use the !register command again.")
        return 

    return True




load_dotenv()
TOKEN = os.getenv("API_TOKEN")
client.run(TOKEN)
