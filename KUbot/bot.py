import os
import discord
from discord.ext import commands
from discord import Colour
from dotenv import load_dotenv
import time
from pymyku.utils import extract
import pymyku
from utils import *
import random

#Load bot token
load_dotenv()
TOKEN = os.getenv("API_TOKEN")

#Colors for each day of the week
DAY_COLORS = {
    'MON': Colour.yellow(),
    'TUE': Colour.pink(),
    'WED': Colour.green(),
    'THU': Colour.orange(),
    'FRI': Colour.blue(),
    'SAT': Colour.purple(),
    'SUN': Colour.red()
}

#Set up the Discord bot
intents = discord.Intents.all()
intents.message_content = True  

client = commands.Bot(command_prefix='!', intents=intents)
user_data = {} #User data container

@client.event
async def on_ready():
    print("KUbot is now online!")

#Resond pong! with time it take in ms
@client.command()
async def ping(ctx):
    start_time = time.time()
    message = await ctx.send("Pong!")  
    end_time = time.time()
    duration_ms = (end_time - start_time) * 1000
    await message.edit(content=f"Pong! Round-trip time: {duration_ms:.2f} ms")

# Not use
# @client.command()
# async def join(ctx):
#     if ctx.author.voice:
#             channel = ctx.author.voice.channel
#             await channel.connect()
#     else:
#         await ctx.send("You are not in a voice channel.")

# @client.command()
# async def leave(ctx): 
#     if ctx.voice_client and ctx.voice_client.guild == ctx.guild: 
#         channel_left = ctx.author.voice.channel
#         await ctx.voice_client.disconnect()
#         await ctx.send(f"I has left from {channel_left} channel")
#     else:
#         await ctx.send("I am not in a voice channel.")
   
#register command 
@client.command()
async def register(ctx):
    user = ctx.author #get user name 
    user_id = ctx.author.id #get user id
    if user_id in user_data:
        await ctx.send("You already register!")
        return
    await user.send("Disclaimer: This project is created for programming concepts project, and we don't collect your username or password.") #Disclaimer
    await user.send("Please provide your username and password in the following format: Username:Password")
    
    def check(msg):
        return msg.author == user and msg.channel.type == discord.ChannelType.private  #Check is message from dm is the same user who call the command
    
    response_msg = await client.wait_for('message', check=check, timeout=300) #Wait user to response
    try:
        username, password = response_msg.content.split(':') 
        ku_client = pymyku.Client(username, password)
        course = ku_client.fetch_group_course() 
        edu = ku_client.fetch_student_education() 
        api_call_time = time.time() #Get time that api is called
        user_data[user.id] = {
            "last_api_call": api_call_time
        }
        if course.get('message') == 'Data Not Found': 
            user_data[user_id]['Timetable'] = None
        else:
            timetable = create_timetable(course)
            user_data[user_id]['Timetable'] = timetable
        if edu.get('message') == 'Data Not Found':
            user_data[user_id]['Education'] = None
        else:
            education_data = edu_data(edu)
            user_data[user_id]['Education'] = education_data

    except:
        await user.send("Something went wrong!")
        return

    await user.send("Successfully registered!")
    print("register command called")

#Send the next class
@client.command()
async def next(ctx): 
    user_id = ctx.author.id 
    if not await user_check(ctx, user_id): #Check if user is registered
        return
    user_info = user_data[user_id] 
    Timetable = user_info["Timetable"]
    if Timetable is None:
        await ctx.send("No timetable data available.")
        return
    upcoming_class, current_day = get_upcoming_class(Timetable)

    #Create embed
    if upcoming_class:
        embed = discord.Embed(title="Next Class", description = upcoming_class['Subject'], color = DAY_COLORS[current_day])
        embed.add_field(name="Class start time", value=f"<t:{upcoming_class['UnixStartTime']}>", inline=False)
        embed.add_field(name="Time until class start", value=f"<t:{upcoming_class['UnixStartTime']}:R>", inline=False)
        embed.add_field(name="Room", value= upcoming_class['Room'], inline=False)
    else:
        embed = discord.Embed(title="No upcoming class today.", color = DAY_COLORS[current_day])

    #Send the embed
    await ctx.send(embed=embed)
    print("Next command called")

#Send a list of classes that the user has
@client.command()
async def table(ctx):
    user_id = ctx.author.id
    if not await user_check(ctx, user_id):
            return

    user_info = user_data[user_id]
    Timetable = user_info.get("Timetable")

    if Timetable is None:
        await ctx.send("No timetable data available.")
    else:
        await ctx.send(Timetable)

#Send User education data
@client.command()
async def mydata(ctx):
    user_id = ctx.author.id
    if not await user_check(ctx, user_id):
            return
    edu_embed = create_education_embed(user_data[user_id]['Education'])
    await ctx.send(embed=edu_embed)

#Send a random number
@client.command()
async def rng(ctx, max : int = 10):
    random_number = random.randint(0, max)
    await ctx.send(random_number)

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



#Run the bot
client.run(TOKEN)
