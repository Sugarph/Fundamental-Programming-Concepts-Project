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
api_timeout_day = 15
user_data = {} #User data container

#Set up Discord bot
intents = discord.Intents.all()
intents.message_content = True  
client = commands.Bot(command_prefix='!', intents=intents)
#Load bot token
load_dotenv()
TOKEN = os.getenv("API_TOKEN")


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
        #course = {"code": "success", "results": [{"peroid_date": "26/06/2566-20/10/2566", "course": [{"section_id": 229512, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01999111-64", "subject_name_th": "ศาสตร์แห่งแผ่นดิน", "subject_name_en": "Knowledge of the Land", "section_code": "804", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "นัฎฐวิกา จันทร์ศรี,จิรเกียรติ ทรายทอง", "teacher_name_en": "Chirakiat Saithong,Natthavika Chansri", "day_w_c": "1000000", "time_from": "8:00", "time_to": "10:00", "day_w": "MON ", "room_name_th": "อาคาร 13 พลศึกษา", "room_name_en": "อาคาร 13 พลศึกษา", "time_start": 480}, {"section_id": 228965, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01418112-65", "subject_name_th": "แนวคิดการโปรแกรมเบื้องต้น", "subject_name_en": "Fundamental Programming Concepts", "section_code": "800", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "ฉัตรชัย เกษมทวีโชค", "teacher_name_en": "Chatchai Kasemtaweechok", "day_w_c": "0100000", "time_from": "10:00", "time_to": "12:00", "day_w": "TUE ", "room_name_th": "17301", "room_name_en": "17301", "time_start": 600}, {"section_id": 228972, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01418141-65", "subject_name_th": "ทรัพย์สินทางปัญญาและจรรยาบรรณวิชาชีพ", "subject_name_en": "Intellectual Properties and Professional Ethics", "section_code": "800", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "อรวรรณ วัชนุภาพร,เฟื่องฟ้า เป็นศิริ", "teacher_name_en": "Fuangfar Pensiri,Orawan Watchanupaporn", "day_w_c": "0010000", "time_from": "9:00", "time_to": "12:00", "day_w": "WED ", "room_name_th": "17210", "room_name_en": "17210", "time_start": 540}, {"section_id": 228777, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01417111-65", "subject_name_th": "แคลคูลัส I", "subject_name_en": "Calculus I", "section_code": "800", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "จุฬาลักษณ์ แก้วหวังสกูล", "teacher_name_en": "Julalak Kaewwangsakoon", "day_w_c": "0010000", "time_from": "13:00", "time_to": "16:00", "day_w": "WED ", "room_name_th": "1408/1", "room_name_en": "1408/1", "time_start": 780}, {"section_id": 228963, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01418111-65", "subject_name_th": "วิทยาการคอมพิวเตอร์เบื้องต้น", "subject_name_en": "Introduction to Computer Science", "section_code": "800", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "สุชาดา ชมจันทร์", "teacher_name_en": "Suchada Chomjan", "day_w_c": "0010000", "time_from": "16:30", "time_to": "18:30", "day_w": "WED ", "room_name_th": "17201", "room_name_en": "17201", "time_start": 990}, {"section_id": 228966, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01418112-65", "subject_name_th": "แนวคิดการโปรแกรมเบื้องต้น", "subject_name_en": "Fundamental Programming Concepts", "section_code": "830", "section_type": "16902", "section_type_th": "ปฏิบัติ", "section_type_en": "Laboratory", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "ฉัตรชัย เกษมทวีโชค", "teacher_name_en": "Chatchai Kasemtaweechok", "day_w_c": "0001000", "time_from": "8:00", "time_to": "10:00", "day_w": "THU ", "room_name_th": "26512", "room_name_en": "26512", "time_start": 480}, {"section_id": 227180, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01999021-64", "subject_name_th": "ภาษาไทยเพื่อการสื่อสาร", "subject_name_en": "Thai Language for Communication", "section_code": "803", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "โกวิทย์ พิมพวง,อาจารย์พิเศษ .", "teacher_name_en": "Kowit Pimpuang,Visiting Lecturer ", "day_w_c": "0001000", "time_from": "16:30", "time_to": "19:30", "day_w": "THU ", "room_name_th": "17401", "room_name_en": "17401", "time_start": 990}, {"section_id": 233683, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "01355209-64", "subject_name_th": "ภาษาอังกฤษเพื่อการสื่อสารในงานอาชีพ", "subject_name_en": "Communicative English for Careers", "section_code": "802", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "บัณฑิตา สันติกุล", "teacher_name_en": "Bandita Santikul", "day_w_c": "0000100", "time_from": "9:00", "time_to": "12:00", "day_w": "FRI ", "room_name_th": "17207", "room_name_en": "17207", "time_start": 540}, {"section_id": 227268, "groupheader": "26/06/2566-20/10/2566", "weekstartday": "2023-06-26T00:00:00.000Z", "weekendday": "2023-10-20T00:00:00.000Z", "std_id": "246115", "subject_code": "03751112-64", "subject_name_th": "สังคมและการเมือง", "subject_name_en": "Social and Politics", "section_code": "801", "section_type": "16901", "section_type_th": "บรรยาย", "section_type_en": "Lecture", "student_status_code": "17001", "std_status_th": "ปกติ", "std_status_en": "Regular", "teacher_name": "เติมศักดิ์ สุขวิบูลย์", "teacher_name_en": "Toemsak Sukhvibul", "day_w_c": "0000100", "time_from": "13:00", "time_to": "16:00", "day_w": "FRI ", "room_name_th": "17305", "room_name_en": "17305", "time_start": 780},{"section_id":999999,"groupheader":"26/06/2566-20/10/2566","weekstartday":"2023-06-26T00:00:00.000Z","weekendday":"2023-10-20T00:00:00.000Z","std_id":"246115","subject_code":"TEST-123","subject_name_th":"Test","subject_name_en":"Test","section_code":"999","section_type":"99999","section_type_th":"Test","section_type_en":"Test","student_status_code":"17001","std_status_th":"ปกติ","std_status_en":"Regular","teacher_name":"Test Teacher","teacher_name_en":"Test Teacher","day_w_c":"0000010","time_from":"11:30","time_to":"12:30","day_w":"SAT ","room_name_th":"Test Room","room_name_en":"Test Room","time_start":690}]}], "cache": True}
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
    print("Table command called")

#Send User education data
@client.command()
async def mydata(ctx):
    user_id = ctx.author.id
    if not await user_check(ctx, user_id):
            return
    edu_embed = create_education_embed(user_data[user_id]['Education'])
    await ctx.send(embed=edu_embed)
    print("Mydata command called")

#Send a random number
@client.command()
async def rng(ctx, max : int = 10):
    random_number = random.randint(0, max)
    await ctx.send(random_number)
    print("Rng command called")

@client.command()
async def rps(ctx, user_input: int):
    rps = ["🪨", "📄", "✂️"]
    await ctx.send(f"You choose:{rps[user_input]}")
    
    if user_input < 0 or user_input > 2:
        print("Please type in 0-2")
        return
    com_choice = random.randint(0, 2)
    await ctx.send(f"Computer choose:{rps[com_choice]}")
    if user_input == 0 and com_choice == 2:
        await ctx.send("You win!")
    elif com_choice == 0 and user_input == 2:
        await ctx.send("You lose")
    elif com_choice > user_input:
        await ctx.send("You lose")
    elif user_input > com_choice:
        await ctx.send("You win!")
    elif com_choice == user_input:
        await ctx.send("It's a draw")


#Check if user is registered or not
async def user_check(ctx, user_id):
    if user_id not in user_data:
        await ctx.send("You are not registered. Please use the !register command.")
        return 

    user_info = user_data[user_id]
    last_api_call = user_info.get("last_api_call", 0)
    current_time = time.time()

    if current_time - last_api_call >= 86400 * api_timeout_day:
        await ctx.send("It's been more than 1 day since the last data update. Please use the !register command again.")
        return 

    return True



#Run the bot
client.run(TOKEN)
