
# Missing data Alerts

The service requires input data  from utility meters exported to csv file. Readings between specified dates and occupancy hours are extracted and processed in the way that allows to record events of continous data gaps icluding timestamps and duration. Output of the service is saved to json file and email notification send to provided recipient. 


# Input Data 

Input data must be in csv format and include following columns: timestamp, meter, energy_kwh. <br />
Data can include readings from multiple meters as long as the meters are labeled. 

# Configuration of the service 

Configuration can be changed by editing SERVICE CONFIGURATION section in main.py. Following parameters can be specified by the user: 
1. facility_name - usually name of the building or group of buildings 
2. start_date, end_date - specific dates between the missing data will be extracted. If you want to run periodic task automatically use the second option when end_day is present timestamp (now= datetime.now()), and use the number of days in timedelta to find start_date( now - timedelta(days=7)). To use that option you need to make sure that recent meters data was exported to data directory. 

# Configure gmail account to send emails

https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
