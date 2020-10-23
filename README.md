# FM e-services background

The project contains facility management e-services developed as a part of Knowledge Transfer Partnership between Strathclyde University (https://www.strath.ac.uk/) and arbnco Ltd (https://us.arbnco.com/).  Proposed solutions are data driven services, that were based on energy consumption data from utility meters at Strathclyde University and data from IEQ monitoring for some commercial buildings. Additionally, data from publicly accessible API was used to deliver information related to weather conditions.
This project contains backend data processing applications and there is no graphic user interface. The e-services can be run from the command window, cron (Linux) or task scheduler (Windows). Applications can be incorporated in existing dashboards using API and background jobs. The scope of this project was limited to raw data processing and functionality of services is shown on the graph below:


![Flow chart of e-services ](/images/schema_01.png)

There are 4 type of services in this repository:
*	Missing Data Alerts
* Adverse CO2 concentration
*	PV performance ratio
*	Building zones energy share


# Installation 

1. The services were created with Python 3.7.5, please ensure you have a similar version installed on your local machine. You can check your Python version by opening a Command Prompt window and typing `python -V`. If Python is not installed, it can be downloaded from the Python for Windows website (try and use the x86-64 version where possible).

2. Download source code by choosing Code->Download ZIP and extract files to C:\ on your local machine (do not choose alternative one as there is a reference to this specific location in the main.py file)

![Download_package ](/images/img_02.png)


3.	A requirements.txt file has been supplied with all the necessary libraries required to use this tool. Use Command Prompt to navigate to the -eservices directory 

`cd C:\FM_e-services-main` and use `pip install -r requirements.txt` to ensure all requirements are present.
