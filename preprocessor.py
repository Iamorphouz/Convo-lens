import re
import pandas as pd


def preprocess(data):
    check = re.split(r' -', data, 1)
    # print(check)
    pattern = r'\d{2}/\d{2}/\d{2},\s\d{2}:\d{2} - '
    if 'm' in check[0].lower():
        # print(1)
        pattern = r'\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s\w{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    # len(messages)

    dates = re.findall(pattern, data)

    # Forming DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    # convert message_data type

    try:  # 12hrs
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %I:%M %p - ')
        # df['message_date'] = df['message_date'].dt.strftime('%d/%m/%y %I:%M %p')
    except ValueError:  # 24hrs
        df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # separate users and messages
    users = []
    messages = []

    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message.strip())
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # print(type(df['year']))

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year.astype(str).str.zfill(4)
    # df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df

