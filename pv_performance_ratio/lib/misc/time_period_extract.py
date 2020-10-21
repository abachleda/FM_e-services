import datetime as dt
from datetime import datetime
import pandas as pd
import json
import os
#Import data from json files in known directory, defaul period of time is 1 week 
#put the data into the events array 

def time_period_extract(end_date,days=7):
    week_times=[]
    week_ago = datetime.strptime(end_date,'%Y-%m-%d %H:%M:%S') - dt.timedelta(days)
    datelist = pd.date_range(week_ago, periods=days+1).tolist()
    for i in datelist:
        week_times.append(str(i.strftime('%Y-%m-%d')))
    return week_times