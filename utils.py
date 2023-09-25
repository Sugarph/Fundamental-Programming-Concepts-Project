import datetime


def get_monday_midnight():
    # Get the current date and time
    now = datetime.datetime.now()

    days_until_current_monday = now.weekday()

    # Calculate the current Monday midnight
    current_monday_midnight = datetime.datetime(now.year, now.month, now.day) - datetime.timedelta(days=days_until_current_monday)

    # Convert the current Monday midnight to Unix time
    unix_time = int(current_monday_midnight.timestamp())
    return unix_time



def convert_to_unix(day_of_week, time_str):
    monday_midnight = get_monday_midnight()
    start_time, end_time = time_str.split(' - ')
    start_hour, start_minute = map(int, start_time.split(':'))
    end_hour, end_minute = map(int, end_time.split(':'))

    # Calculate seconds since Monday midnight (start of the week)
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
    
    print(schedule_by_day) #Debug
    
