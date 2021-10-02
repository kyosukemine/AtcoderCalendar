from __future__ import print_function
import datetime


import pandas as pd
import datetime


def omit(S):
    S_ = S
    S_ = S_.replace('AtCoder Beginner Contest','ABC')
    S_ = S_.replace('AtCoder Regular Contest','ARC')
    S_ = S_.replace('AtCoder Heuristic Contest','AHC')
    S_ = S_.replace('Programming Contest','PC')
    S_ = S_.replace(year,'')
    S_ = S_.replace('◉  ','')
    S_ = S_.replace(' ','')
    return S_


today = datetime.date.today()
year = today.strftime('%Y')
old_df = pd.read_csv('old.csv')
url =  'https://atcoder.jp/contests'
df = pd.read_html(url)
StartTime = []
ContestName = []
Duration = []
EndTime = StartTime + Duration
print(df[2])
for tstr, dstr, name in zip(df[1]['Start Time (local time)'],df[1]['Duration'], df[1]['Contest Name']):
    s = datetime.datetime.strptime(tstr, '%Y-%m-%d %H:%M:%S%z')
    StartTime.append(s.isoformat())
    h, m = map(int,dstr.split(':'))
    d = h + m / 60
    EndTime.append((s + datetime.timedelta(hours=d)).isoformat())
    omitedname = omit(name)
    ContestName.append(omitedname)