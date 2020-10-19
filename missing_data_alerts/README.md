
# Missing data Alerts

The service requires input data  from utility meters exported to csv file. Readings between specified dates and occupancy hours are extracted and processed in the way that allows to record events of continous data gaps (NaN, 0), icluding timestamps and duration. Output of the service is saved to json file and email notification send to provided recipient. 


# Input Data 

Input data must be in csv format and include following columns: timestamp, meter, energy_kwh. <br />
Data can include readings from multiple meters/buildings  as long as the meters are labeled. 

# Configuration of the service 

Configuration can be changed by editing SERVICE CONFIGURATION section in main.py. Following parameters can be specified by the user: 
1. facility_name - usually name of the building or group of buildings 
2. start_date, end_date - specific dates between the missing data will be extracted. If you want to run periodic task automatically use the second option when end_day is present timestamp (now= datetime.now()), and use the number of days in timedelta to find start_date( now - timedelta(days=7)). To use that option you need to make sure that recent meters data is also automatically exported to data directory. 
3. start+occupany_hour, end_occupancy_hour - define the hours when building occupied and energy consumption equal to 0 is not a possibility. 
4. interval_datapoint_minutes -  Interval betweeen energy consumption readings according to datased. This is usually equal to 30 minutes for most of meters in commercial buildings. 
5. submeters - List including submeters from the data set, that you want to consider. 
6. meters_labels - Specific labels assigned to the meters in data file. That could be buildings names if the meters are per building. 
7. recipient_email_address -  Recipient email adress for electronic alerts notification. Note that the SNMP server needs to be configured.

# Configure gmail account to send emails

Service is configured to send email notification to provided recipient, however SNMP server needs to be configured. Please reffer to: 
https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development

After SNMP server configured, In order to send emails  please provide credentials in the /lib/send_email.py :  <br />
<configured_email>, <gmail_password>, <smtp_server>, <smtp_port>. <br />

To use gmail SMTP use: <br />
smtp_server='smtp.gmail.com' <br />
smtp_port=465


