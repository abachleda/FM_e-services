
# Declare the working directory 
import sys
import os
sys.path.append('C:/FM_e-services-main/missing_data_alerts')
os.chdir('C:/FM_e-services-main/missing_data_alerts')
# Inport libraries
import pandas as pd
from datetime import datetime,timedelta
import json
# Custom functions
from lib.send_email import send_email
#custom functions 
from lib.extract_annomalies import extract_annomalies

#%%SERVICE CONFIGURATION INPUT VARIABLES##
facility_name='Campus X'
#required data format str yyyy-mm-dd hh:mm:ss
start_date='2020-03-01 00:00:00'
end_date='2020-03-24 23:30:00'

# Option if the service is run trough cron or task scheduler in daily basis. Data with current readings needs to be available to run that option (data/energy_data.csv)
'''now=datetime.now()
start_date=now.strftime("%Y-%m-%d %H:%M:%S")
end_date=(now-timedelta(days=1)).strftime("%Y-%m-%d %H:%M:%S")'''

#required hour formal str hh:mm
start_occupancy_hour='06:30'
end_occupancy_hour='18:30'

#frequency of measurment
interval_datapoint_minutes=30
# treshold for triggering missing data alert ( in minutes) 
alert_threshold_minutes=120


#list of the submeters considered in analysis 
submeters = ['HM-CU-01','HM-HW-01','HM-JW-01','HM-JA-01','HM-RW-01','HM-RC-01','HM-ST-01','HM-SU-01','HM-TG-01','HM-TI-01','HM-SC-01','HM-GH-01','HM-HD-01','HM-TG-02','HM-TG-03']

# assigned building names to the meter names included in data 
meters_labels= {
    'HM-CU-01':'Building_1',
    'HM-HW-01':'Building2',
    'HM-JW-01':'Building_3',
    'HM-JA-01':'Building_4',
    'HM-RW-01':'Building_5',
    'HM-RC-01':'Building_6',
    'HM-ST-01':'Building_7',
    'HM-SU-01':'Building_8',
    'HM-TG-01':'Building_9',
    'HM-TI-01':'Building_10',
    'HM-SC-01':'Building_11',
    'HM-GH-01':'Building_12',
    'HM-HD-01':'Building_13', 
    'HM-TG-02':'Building_14',
    'HM-TG-03':'Building_15'
    }

recipient_email_address= '<provide_recipient_email?'

#%% Data Perocessing 
#current timestamp 
current_timestamp=datetime.now()
current_timestamp_string =datetime.now().strftime('%Y-%m-%d %H:%M:%S')


#Export data from csv file 
energy_data = pd.read_csv('data/energy_data.csv')
#change timestamp to datetime
energy_data['timestamp']=pd.to_datetime(energy_data['timestamp'])
#sort by timestamp
energy_data=energy_data.sort_values(by=['timestamp'])
 
####Extract period of time defined by the user####

mask = (energy_data['timestamp'] >= start_date) & (energy_data['timestamp'] <= end_date)
energy_data = energy_data.loc[mask]
energy_data=energy_data.reset_index(drop=True)

#extract data from meters specified in the configuration (submeters) 
energy_data=energy_data.loc[energy_data['meter'].isin(submeters)] 

#choose only energy readings column 
energy_data=energy_data[['meter','energy_kwh','timestamp']]

####Transform dataframe####

#drop duplicates in dataframe 
energy_data=energy_data.drop_duplicates()
#transform to multiple columns 
energy_data=energy_data.pivot(index='timestamp',columns='meter',values='energy_kwh' )

#rename columns for names of the buildings that has specific meter installed (meters_labels) 
energy_data.rename(columns=meters_labels,inplace=True)
#choose only timestamps during occupancy hours 
energy_data1=energy_data.between_time(start_occupancy_hour, end_occupancy_hour)
#save buildings names in the array 
buildings_list=list(energy_data1)
#reset index 
energy_data1=energy_data1.reset_index()


#%%DETECT INCORRECT 0  OR NAN READINGS  IN THE DATA DURING OCCUPANCY HOURS#######  
#%%define dictionary to store erroneous data
data={}
data['zero_data']={'timestamp':current_timestamp_string}
data['zero_data'].update({'zero_readings_values':{}})

data['nan_data']={'timestamp':current_timestamp_string}
data['nan_data'].update({'nan_readings_values':{}})

buildings_name_zero_data=[]
buildings_name_nan_data=[]


for building in buildings_list:
    dataframe=energy_data1[['timestamp',building]]
    #check for empty values
    dataframe_zero_values= dataframe[['timestamp',building]][dataframe[building]==0]
    dataframe_nan_values= dataframe[['timestamp',building]][dataframe[building].isnull()]
    #sort by timestamp 
    dataframe_zero_values= dataframe_zero_values.sort_values(by='timestamp',ascending=True)
    dataframe_nan_values= dataframe_nan_values.sort_values(by='timestamp',ascending=True)
    #Extracting 0  values reported and duration of the annomaly
    if not dataframe_zero_values.empty:
        data['zero_data']['zero_readings_values'].update({building:[]})
        data['zero_data']['zero_readings_values'][building]=extract_annomalies(
            dataframe_anomalies=dataframe_zero_values,
            interval_minutes=interval_datapoint_minutes,
            output_dictionary=data['zero_data']['zero_readings_values'][building],
            name='zero_values')
        buildings_name_zero_data.append(building)
    #Extracting 0  values reported and duration of the annomaly        
    if not dataframe_nan_values.empty:
        data['nan_data']['nan_readings_values'].update({building:[]})
        data['nan_data']['nan_readings_values'][building]=extract_annomalies(
            dataframe_anomalies=dataframe_nan_values,
            interval_minutes=interval_datapoint_minutes,
                      output_dictionary=data['nan_data']['nan_readings_values'][building],
                      name='nan_values')
        buildings_name_nan_data.append(building)


#%%RISE ALERT IF 0 READIINGS RECORDED FOR LONGER THAN SPECIFIED THRESHOLD OR ANY NaN READINGS RECORDED ########
#array to store alerts 
recorded_alerts={}
#save report date as current timestamp 
report_date=current_timestamp_string
formated_date = report_date[0:10]+'_'+report_date.replace(':',"_")[11:]

for building in buildings_name_zero_data: 
    for i in data['zero_data']['zero_readings_values'][building][0]:
        if int(i['duration'])>alert_threshold_minutes:
            timestamp=i['anomalies_details'][-1][0]
            alert={timestamp: 'Zero values recorded for the period of '+i['duration']+' minutes during normal occupancy hours in ' +building}
            recorded_alerts.update(alert)

for building in buildings_name_nan_data: 
    for i in data['nan_data']['nan_readings_values'][building][0]:
        timestamp=i['anomalies_details'][-1][0]
        alert={timestamp:'Missing values recorded for the period of '+i['duration']+' minutes during normal occupancy hours in ' +building}
        recorded_alerts.update(alert)
## save alerts in json output 

with open('output/'+formated_date+'.json', 'w') as fp:
    json.dump(recorded_alerts, fp)   
#%%SEND EMAIL NOTIFICATION IF ANY ALERTS RECORDED#####
if len(recorded_alerts)>0: 
    alerts=''
    for i in recorded_alerts: 
        alerts=alerts+i+' '+recorded_alerts[i][:]+'\n\n'
    content=' Missing data events detected. Check the details below: \n\n'+alerts
    send_email(
            content,
			#Fill email address 
            receivers = recipient_email_address,
            subject = 'Missing data events detected for energy meters at '+facility_name,
            file_location = None,
            file_name = None
            )

