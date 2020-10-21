# Submeters Energy Share 
The service requires input data from building submeters exported to csv file. Share of each meter in total energy consumption is calculated and displayed in report with a table and treemap graph. The report is sent to provided recipient email. 

# Input Data 

Input data from building submeters must be in csv format and include following columns: timestamp, meter, energy_kwh. <br />

Note: If you want to run this service in regular intervals you need to make sure that that the submeters data is also exported in requilar basis to /data/energydata.csv
eg. if you want to run this service every week data from last week needs to be exported to /data/energydata.csv  before scheduled time of the service run. 


# Configuration of the service 

Configuration can be changed by editing SERVICE CONFIGURATION section in main.py. Following parameters can be specified by the user: 

*meters
