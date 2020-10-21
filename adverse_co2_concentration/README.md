# Adverse CO2 Concenration

The service requires input data from IEQ sensors exported to csv file. It processes input data and allow to extract and visualise adverse adverse conditions recorded by sensors, including timeframes and duration of the condition. 


# Input Data 

Input data from IAQ sensors (/data/co2_data.csv) must be in csv format and include following columns: timestamp, site_label,device_label, co2. <br />

Note: If you want to run this service in regular intervals you need to make sure that that the IEQ sensors  is also exported in requilar basis to /data/co2_data.csv
eg. if you want to run this service every week data from last week needs to be exported to /data/co2_data.csv before scheduled time of the service run. 


# Configuration of the service 

Configuration can be changed by editing SERVICE CONFIGURATION section in main.py. Following parameters can be specified by the user: 

1. upper_bound- Critical threshold for CO2 level. Above this value conditions in the space are considered to be adverse
2. interval_datapoints -  Reading frequency as in input data file. 


# Output data

The output of the service include json file with adverse CO2 levels registered by sensors and stored in /output . The information include timestamp, duration of adverse conditions. Additionaly a timeline graphs with adverse condition visualisation for each device are saved in /output/charts.  
