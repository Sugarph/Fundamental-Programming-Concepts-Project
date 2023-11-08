import time
from datetime import datetime
import datetime


def get_monday_midnight():
    now = datetime.datetime.now()

    days_until_current_monday = now.weekday()

    # Calculate the current Monday midnight
    current_monday_midnight = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=days_until_current_monday)
    unix_time = int(current_monday_midnight.timestamp())
    return unix_time



def convert_to_unix(day_of_week, time_str):
    monday_midnight = get_monday_midnight()
    start_time, end_time = time_str.split(' - ')
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))

    # Calculate seconds since Monday midnight
    seconds_since_monday_midnight = day_of_week * 86400 + start_hour * 3600 + start_minute * 60
    start_unix = seconds_since_monday_midnight
    end_unix = seconds_since_monday_midnight + (end_hour - start_hour) * 3600 + (end_minute - start_minute) * 60

    return start_unix + monday_midnight, end_unix + monday_midnight


def schedule_unix(schedule):
    schedule_by_day = {}

    for item in schedule:
        day = item['Day']
        if day not in schedule_by_day:
            schedule_by_day[day] = []
        schedule_by_day[day].append({
            'Subject': item['Subject'],
            'Time': item['Time'],
            'Room': item['Room']
        })
    
    for day, subjects in schedule_by_day.items():
        day_of_week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN'].index(day)
        
        for subject in subjects:
            start_unix, end_unix = convert_to_unix(day_of_week, subject['Time'])
            subject['UnixStartTime'] = start_unix
            subject['UnixEndTime'] = end_unix
            del subject['Time']

    return schedule_by_day 

#create timetable from API response
def create_timetable(api_response):
    timetable = []

    for course in api_response['results'][0]['course']: 
        subject_name_th = course['subject_name_th']
        subject_name_en = course['subject_name_en']
        day_w = course['day_w'].strip()
        time_from = course['time_from']
        time_to = course['time_to']
        room_name_th = course['room_name_th']
        room_name_en = course['room_name_en']

        timetable_entry = f"Subject: {subject_name_en}, Day: {day_w}, Time: {time_from} - {time_to}, Room: {room_name_en}"
        timetable.append(timetable_entry)
    

    return '\n'.join(timetable) #Create newline every subject


def edu_data(data):
    education_data = data["results"]["education"][0]
    
    edulevelNameEn = education_data['edulevelNameEn']
    statusNameEn = education_data['statusNameEn']
    degreeNameEn = education_data['degreeNameEn']
    typeNameEn = education_data['typeNameEn']
    campusNameEn = education_data['campusNameEn']
    curNameEn = education_data['curNameEn']
    facultyNameEn = education_data['facultyNameEn']
    majorNameEn = education_data['majorNameEn']
    majorCode = education_data['majorCode']
    stu_data = f"Education Level: {edulevelNameEn}, Status: {statusNameEn}, Degree: {degreeNameEn}, Type: {typeNameEn}, Campus: {campusNameEn}, Curriculum: {curNameEn}, Faculty: {facultyNameEn}, Major: {majorNameEn}, Major Code: {majorCode}"
    return stu_data

def extract_subject_info(timetable):
    subjects = timetable.strip().split('\n')
    schedule = []

    for subject in subjects:
        parts = subject.strip().split(', ')
        subject_info = {}
        for part in parts:
            key, value = part.split(': ')
            subject_info[key] = value
        schedule.append(subject_info)

    return schedule

def get_upcoming_class(timetable):
    subject_schedule = extract_subject_info(timetable)
    schedule = schedule_unix(subject_schedule)
    current_date = datetime.datetime.now()
    current_day = current_date.strftime('%a').upper()
    current_time = int(time.time())
    classes_today = schedule.get(current_day, [])

    for cls in classes_today:
        if cls['UnixEndTime'] > current_time:

            end_time = cls['UnixEndTime']
            return cls, current_day
    

    
    return None, current_day


