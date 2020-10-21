# Adverse CO2 Concenration

The service requires input data from IEQ sensors exported to csv file. It processes input data and allow to extract and visualise adverse conditions recorded by sensors, including timeframes and duration of the condition.

# Input Data 

Input data from IAQ sensors (/data/co2_data.csv) must be in csv format and include following columns: timestamp, site_label, device_label, co2. 
Note: If you want to run this service in regular intervals you need to make sure that that the IEQ sensors is also exported in regular basis to /data/co2_data.csv e.g. if you want to run this service every week data from last week needs to be exported to /data/co2_data.csv before scheduled time of the service run.


# Configuration of the service 

Configuration can be changed by editing SERVICE CONFIGURATION section in main.py. Following parameters can be specified by the user:
1.	upper_bound- Critical threshold for CO2 level. Above this value conditions in the space are considered as adverse. 
2.	interval_datapoints - Reading frequency as in input data file.


# Output data

The output of the service includes json file, with adverse CO2 levels registered by sensors and stored in /output. The information include timestamp, duration of adverse conditions. Additionally, a timeline graphs with adverse condition visualisation for each device are saved in /output/charts.

# How to run service

After all required packages were installed on the local machine e-services can be either run from command window (1) or added to Task Scheduler and run as a periodic task (2).
1.	Open cmd and navigate to specific service location using: 
cd C:/KTP_e-services-master/adverse_co2_concentration 
py main.py
2.	Add a periodic task to Task Scheduler providing action start program: 
C:\KTP_e-services-master\adverse_co2_concentration\adverce_co2_concentration.bat

