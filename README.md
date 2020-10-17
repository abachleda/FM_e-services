# KTP_e-services background
The project contains facility management e-services developed as a part of Knowladge Transfer Partnership between Strathclyde University and arbnco. Proposed sollutions are data driven services, that were based on energy consumption data from utility meters at Strathclyde University and data from IEQ monitoring for some commercial buildings. Additionaly data from publicly accessible API was used to deliver information related to weather conditions and local carbon intensity of the local electrical grid. 

This project contains backend data processing applications and there is no graphic user interface. The e-services can be run from the command window, cron (Linux) or task scheduler(Windows). Applications can be incorporated in existing dashboards using API and backgroud jobs. The scope of this project was limited to raw data processing and functionality of services is shown on the graph below: 

![Flow chart of e-services ](/images/schema_01.png)


# Installation 

The services were created with Python 3.7.5, please ensure you have a similar version installed on your local machine. You can check your Python version by opening a Command Prompt window and typing python -V. If Python is not installed, it can be downloaded from the Python for Windows website (try and use the x86-64 version where possible).
