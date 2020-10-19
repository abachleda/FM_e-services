
# Missing data Alerts

The service requires input data  from utility meters exported to csv file. Readings between specified dates and occupancy hours are extracted and processed in the way that allows to record events of continous data gaps icluding timestamps and duration. Output of the service is saved to json file and email notification send to provided recipient. 


# Input Data 

Input data must be in csv format and include following columns: timestamp, meter, energy_kwh. <
# Configure gmail account to send emails

https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development
