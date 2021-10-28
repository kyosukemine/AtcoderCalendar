from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import pandas as pd
import datetime


def omit(S):
    S_ = S
    S_ = S_.replace('AtCoder Beginner Contest','ABC')
    S_ = S_.replace('AtCoder Regular Contest','ARC')
    S_ = S_.replace('AtCoder Heuristic Contest','AHC')
    S_ = S_.replace('AtCoder Grand Contest','AGC')
    S_ = S_.replace('Programming Contest','PC')
    S_ = S_.replace(year,'')
    S_ = S_.replace('◉  ','')
    S_ = S_.replace(' ','')
    return S_


today = datetime.date.today()
year = today.strftime('%Y')
old_df = pd.read_csv('../old.csv')
url =  'https://atcoder.jp/contests/'
df = pd.read_html(url)
StartTime = []
ContestName = []
Duration = []
EndTime = StartTime + Duration

for tstr, dstr, name in zip(df[1]['Start Time (local time)'],df[1]['Duration'], df[1]['Contest Name']):
    s = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S%z')
    StartTime.append(s.isoformat())
    h, m = map(int,dstr.split(':'))
    d = h + m / 60
    EndTime.append((s + datetime.timedelta(hours=d)).isoformat())
    omitedname = omit(name)
    ContestName.append(omitedname)


cols = ['StartTime', 'EndTime', 'ContestName']
df = pd.DataFrame(index=[], columns=cols)
df['StartTime'] = StartTime
df['EndTime'] = EndTime
df['ContestName'] = ContestName
# new.csvファイルの作成をする
df.to_csv('../old.csv', index=0)

write_calender_df = df[~df.isin(old_df.to_dict(orient='list')).all(1)]

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']



"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.

# if os.path.exists('token.json'):
creds = Credentials.from_authorized_user_file('../token.json', SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    # if not creds and not creds.expired and creds.refresh_token:
    #     flow = InstalledAppFlow.from_client_secrets_file(
    #         'client_secret_1046041032257-va7lnj01fdh5kelhkok5n4g39ed2on1g.apps.googleusercontent.com.json', SCOPES)
    #     creds = flow.run_local_server(port=0)
    # else:
    print("credsが有効じゃないかも")
    flow = InstalledAppFlow.from_client_secrets_file(
        '../client_secret_1046041032257-va7lnj01fdh5kelhkok5n4g39ed2on1g.apps.googleusercontent.com.json', SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('../token.json', 'w') as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)


df = write_calender_df
if not df.empty:
    for s,e,n in zip(df['StartTime'],df['EndTime'],df['ContestName']):
        event = {
        "summary": n,
        "start": {
            "dateTime": s,
            "timeZone": "Asia/Tokyo",
        },
        "end": {
            "dateTime": e,
            "timeZone": "Asia/Tokyo",
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 24 * 60},
                {'method': 'popup', 'minutes': 10},
            ],
            },
        }
        event = service.events().insert(calendarId='upguod47r5vb8dg5jijfo1f3vk@group.calendar.google.com',
                                        body=event).execute()
        print("カレンダー書けたよ!!!!!!")
        print(n)
else:
    print("カレンダー変更なしだよ!!!!!!")

# githubに上げる
# グーグルカレンダーから取得して比較する