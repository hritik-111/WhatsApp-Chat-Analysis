import re
import pandas as pd


def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[ap][m]\s-\s'
    messages = re.split(pattern,data)
    dates = re.findall(pattern,data)
    messages.pop(0)
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
    df.rename(columns={'message_date':'date'}, inplace=True)
    
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split('(\+?\d{0,2}\s?\d{10}|[\w\s]+):\s(.*)', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
            
        else:
            users.append('group_notification')
            messages.append(entry[0])

    # Add the new columns to the dataframe and drop the original column
    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)


    
    df['year'] = df['date'].dt.year
    df['month']=df['date'].dt.month_name()
    df['day']=df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df