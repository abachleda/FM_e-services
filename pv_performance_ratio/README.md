# PV Performance Ratio 
The Service calculates Performance Ratio (PR) of PV system integrated in the building by comparing modelled energy output from PV array with actuall energy output of the system measured by generation meter. 

# Input Data 

Input data must include weather data and energy output readings from generation meter. 
Weather data must include columns: 'timestamp', 'clouds', 'temperature','pressure', 'wind_speed' and 'humidity'
Generation meter data must include columns: 'timestamp'. 'energy_kwh'


Note: If you want to run this service in regular intervals you need to make sure that required data is also exported in requilar basis to /data/
eg. if you want to run this service every week weather data from last week needs to be exported to /data/weather_data.csv and energy generation meter data exported to /data/generation_meter_readings.csv,  before scheduled time of the service run. 


# Configuration of the service 

Configuration can be changed by editing SERVICE CONFIGURATION section in main.py. Following parameters can be specified by the user: 

1. name - Name of the site/building 
2. latitude, longitude, altitude - Geographical coordinates of the site
3. ghi_model -  specifies the model used for ghi estimation, available options: kasten, zhang-huang
4. decomp_model -  specifies decomposition model used for decomposing solar radiation into direct and diffuse components, available_options: dirint, erbs 
5. surface_tilt - Inclination angle of PV installation
6. surface_azimuth - azimuth angle for PV installation 
7. active_area - total active area of PV array in squared meters 
8. efficiency_modules= eficiency of PV modules provided by producer 
9. interval - period of time in days considered in PR calculations 
10. number of days taken into account for PR visualisation 
11. pr_days  - number of days taken into account for visualtisation of historical PR values. 


# Output data

The output of the service include json file with PV energy output and calculated performance ratio stored in  /output/'name'. The information include timestamp, total dc energy modeled and total ac energy generated. Additionaly, generated graphs and reports are stored  in /output/'name'/charts and  /output/'name'/report respectively. 

# Sending e-mails

Service is configured to send email notification to provided recipient, however SNMP server needs to be configured. Please reffer to: 
https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development

After SNMP server configured, In order to send emails  please provide credentials in the /lib/send_email.py :  <br />
<configured_email>, <configured_password>, <smtp_server>, <smtp_port>. <br />

To use gmail SMTP use: <br />
smtp_server='smtp.gmail.com' <br />
smtp_port=465

# How to run service
After all required packages were installed on the local machine e-services can be either run from command window (1) or added to Task Scheduler and run as a periodic task (2). 

1.  Open cmd and navigate to specific service location using: <br />
cd C:\KTP_e-services-master\pv_performance_ratio <br />
ipython main.py

2. Add an a periodic task to Task Scheduler providing action start program: <br /> C:\KTP_e-services-master\pv_performance_ratio\pv_performance_ratio.bat
