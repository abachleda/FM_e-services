# Submeters Energy Share 

The service uses dataset including submeters readings located from the building and visualise the energy consumption share of each submeter in total energy consumption. Automatic report created as an output, includes treemap visualuisation of the results. 

# Input Data 

Input data must be in csv format and include following columns: timestamp , energy_kwh , meter , site. Data can include readings from multiple meters/buildings  as long as the meters and sites are labeled.

# Sending e-mails

Service is configured to send email notification to provided recipient, however SNMP server needs to be configured. Please reffer to: 
https://realpython.com/python-send-email/#option-1-setting-up-a-gmail-account-for-development

After SNMP server configured, In order to send emails  please provide credentials in the /lib/send_email.py :  <br />
<configured_email>, <configured_password>, <smtp_server>, <smtp_port>. <br />

To use gmail SMTP use: <br />
smtp_server='smtp.gmail.com' <br />
smtp_port=465
