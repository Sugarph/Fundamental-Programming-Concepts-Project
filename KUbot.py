import os
import discord
from discord.ext import commands
from discord import Embed, Colour
from dotenv import load_dotenv #import bot token 
import time
import json
from pymyku.utils import extract
import pymyku
from datetime import datetime, timedelta


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
async def table(ctx): 
    user_id = ctx.author.id
    if user_id not in user_data: 
        await ctx.send("You are not registered. Please use the !register command.")
        return 

    user_info = user_data[user_id]
    last_api_call = user_info.get("last_api_call", 0)
    current_time = time.time()
    
    if current_time - last_api_call >= 86400: 
        await ctx.send("It's been more than 1 day since last data update. Please use the !register command again.")
        return

    api_response = user_info["api_response"]
    timetable = create_timetable(api_response)

    subject_schedule = extract_subject_info(timetable)
    target_day = get_next_class_day()
    timetable_embed = create_timetable_embed(subject_schedule, target_day)

    await ctx.send(embed=timetable_embed)
    print("Table command called")



@client.command()
async def register(ctx):
    user = ctx.author
    await user.send("Please provide your username and password in the following format: Username:Password") #Send DMs to user 
    
    def check(msg):
        return msg.author == user and msg.channel.type == discord.ChannelType.private  #Check is message from dm is same user who call the command
    
    response_msg = await client.wait_for('message', check=check, timeout=300) 
    username, password = response_msg.content.split(':')
    ku_client = pymyku.Client(username, password)
    response = ku_client.fetch_group_course()
    api_call_time = time.time()
    user_data[user.id] = {
        "api_response": response,
        "last_api_call": api_call_time
    }

    timetable = create_timetable(response)
    await user.send("Successfully registered!")
    print("register command called")


    
#create timetable from API response
def create_timetable(api_response):
    timetable = []

    for course in api_response['results'][0]['course']: #in api_resoinse in results in course ,it dict in dict in dict ;-;
        subject_name_th = course['subject_name_th']
        subject_name_en = course['subject_name_en']
        day_w = course['day_w'].strip()
        time_from = course['time_from']
        time_to = course['time_to']
        room_name_th = course['room_name_th']
        room_name_en = course['room_name_en']

        # Combine the details into a timetable entry
        timetable_entry = f"Subject: {subject_name_th}, Day: {day_w}, Time: {time_from} - {time_to}, Room: {room_name_th}"
        timetable.append(timetable_entry)
    print(timetable)

    return '\n'.join(timetable) # Join the timetable with newline everytime 

def extract_subject_info(timetable):
    subjects = timetable.strip().split('\n')
    schedule = []

    # Iterate through each subject and extract relevant information
    for subject in subjects:
        parts = subject.strip().split(', ')
        subject_info = {}
        for part in parts:
            key, value = part.split(': ')
            subject_info[key] = value
        schedule.append(subject_info)

    return schedule


def create_timetable_embed(schedule, target_day):
    embed = Embed(title=f'Timetable\nYour class schedule for {target_day}:', color=DAY_COLORS.get(target_day, Colour.default()))

    found = False  # Flag to indicate if any classes were found for the target day

    for subject_info in schedule:
        if subject_info['Day'] == target_day:
            subject_details = f"**Subject:** {subject_info['Subject']}\n**Time:** {subject_info['Time']}\n**Room:** {subject_info['Room']}"
            embed.add_field(name=f"{subject_info['Subject']}", value=subject_details, inline=False)
            found = True  # Set flag to True since we found at least one class for the target day
    
    if not found:
        embed.add_field(name='No classes', value=f'No classes scheduled for {target_day}.', inline=False)

    return embed


def get_next_class_day():
    today = datetime.now().strftime('%a')
    
    if today == 'Sat' or today == 'Sun':
        return 'Mon'
    
    next_day = today
    while next_day == today:
        tomorrow = datetime.now() + timedelta(days=1)
        next_day = tomorrow.strftime('%a')
    
    return next_day
    


load_dotenv()
TOKEN = os.getenv("API_TOKEN")
client.run(TOKEN)
