import os
import sys
# define the base directory 
os.chdir('C:/KTP_e-services-master/adverse_co2_concentration')
sys.path.append('C:/KTP_e-services-master/adverse_co2_concentration')

import pandas as pd
from datetime import datetime
import json
#custom functions 
from lib.extract_annomalies import extract_annomalies
from lib.timeline_days_hours import timeline_days_hours


#%%SERVICE CONFIGURATION###
upper_bound=1000
interval_datapoint_minutes=5

#%%EXPORT CO2 MEASURMENT DATA FROM CSV FILE###


#data file structure 
data_file_path='data/co2_data.csv'
timestamp_column='timestamp'
co2_column='co2'
device_label_column='device_label'

co2_data = pd.read_csv(data_file_path)

#change timestamp to datetime
co2_data['timestamp']=pd.to_datetime(co2_data[timestamp_column])
#save sensor locations
sensor_zones=co2_data.device_label.unique()

#%% DEFINE DICTIONARY TO STORE ANOMALIES###
#save curent timestamp 
current_timestamp=datetime.now()
current_timestamp_string =datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#define outyput anomaly dictionary
data = {}
data['anomalies']=[]
data['anomalies']={'timestamp':current_timestamp_string}
data['anomalies'].update({'anomaly_co2_values':{}})
#%%EXTRACT ANOMALLIES###
zones_anomalies_name=[]
for sensor_zone in sensor_zones: 
    
    #check for empty values 
    dataframe_per_zone=co2_data.loc[co2_data['device_label']==sensor_zone]
    dataframe_per_zone_anomalies= dataframe_per_zone.loc[dataframe_per_zone['co2'] >upper_bound]
    dataframe_per_zone_anomalies=dataframe_per_zone_anomalies.sort_values(by='timestamp',ascending=True)
   
    if not dataframe_per_zone_anomalies.empty:
        data['anomalies']['anomaly_co2_values'].update({sensor_zone:[]})
        data['anomalies']['anomaly_co2_values'][sensor_zone]=extract_annomalies(
            dataframe_anomalies=dataframe_per_zone_anomalies,
            interval_minutes=interval_datapoint_minutes,
            output_dictionary=data['anomalies']['anomaly_co2_values'][sensor_zone],
            name='anomaly_co2_values')
        zones_anomalies_name.append(sensor_zone)
       
#%% SAVE OUTPUT OF SERVICE IN JSON FILE 
#create directory with current timestamp
if not os.path.exists('output/charts/'+current_timestamp_string[0:10]):
    os.makedirs('output/charts/'+current_timestamp_string[0:10], mode=0o777)
if zones_anomalies_name:
    with open('output/anomalies.json', 'w') as fp:
        json.dump(data, fp)
    #%%PLOT TIMELINE GRAPHS SHOWING DURATION OF ANOMALY AND TIME FOR ALL CONSIDERED PERIOD  
    timeline_days_hours(
        interval_frequency=interval_datapoint_minutes,
        all_co2_dataframe=co2_data,
        sensors_with_anomalies=zones_anomalies_name,
        data=data,
        upper_bound=upper_bound,
        destination_path='output/charts/'+current_timestamp_string[0:10]
        )

