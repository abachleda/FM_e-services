# Submeters Energy Share 
The service requires input data from building submeters exported to csv file. Share of each meter in total energy consumption is calculated and displayed in report with a table and treemap graph. The report is sent to provided recipient email. 

# Input Data 

Input data from building submeters must be in csv format and include following columns: timestamp, meter, energy_kwh. <br />

Note: If you want to run this service in regular intervals you need to make sure that that the submeters data is also exported in requilar basis to /data/energydata.csv
eg. if you want to run this service every week data from last week needs to be exported to /data/energydata.csv  before scheduled time of the service run. 


# Configuration of the service 

Configuration can be changed by editing SERVICE CONFIGURATION section in main.py. Following parameters can be specified by the user: 

1. meters - List of all submeters taken into account to be included in report, labels needs to be as in data file 
2. period - period of time taken into account in days
3. recipient_email - Recipient email adress for electronic alerts notification. Note that the SNMP server needs to be configured.


# Output data

The output of the service include json file with calculated submeters share in total energy consumption, stored in /output. The information include timestamp, considered period and all submeters listed with relevant share in total energy consumption of the building. Additionaly there the generated report is saved in the location output/reports. 

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
cd C:/KTP_e-services-master/submeters_energy_share <br />
ipython main.py

2. Add an a periodic task to Task Scheduler providing action start program: <br /> C:\KTP_e-services-master\missing_data_alerts\submeters_energy_share.bat
