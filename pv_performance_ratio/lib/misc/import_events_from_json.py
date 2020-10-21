import datetime as dt
from datetime import datetime
import pandas as pd
import json
import os
#Import data from json files in known directory, defaul period of time is 1 week 
#put the data into the events array 


def import_events_from_json(week_times,path) :  
    events=[]
    for k in week_times: 
        path_to_file=path+k+'.json'
        if os.path.isfile(path_to_file)==True:
           for line in open(path_to_file, 'r'):
               single_alert=json.loads(line)
               print(single_alert)
               events.append(single_alert)        
    return events 