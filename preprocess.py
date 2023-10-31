import re
import pandas as pd

def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APM]{2}\s-\s'
    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)
    df = pd.DataFrame({'user_messages': messages, 'message_date':dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for m in df['user_messages']:
        entry = re.split('([\w\W]+?):\s', m)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['users']=users
    df['messages']=messages

    df.drop(columns=['user_messages'], inplace=True)
    df['year'] = df['date'].dt.year
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    
    # period = []
    # for hour in df['hour']:
    #     if 1 <= hour < 12:
    #         period.append(f"{hour}-{hour+1} AM")
    #     elif hour == 12:
    #         period.append(f"{hour}-1 PM")
    #     else:  # hour == 0
    #         period.append(f"12-1 AM")

    # df['period'] = period

    
    return df