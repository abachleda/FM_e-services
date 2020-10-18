# -*- coding: utf-8 -*-
"""
Created on Wed Feb 26 10:18:11 2020

@author: agnieszka
"""
#The function will devide discovered anomallies into separate arrays and save them to the alert dictionary 
#single anomalies(piks) will be saved each in separate arrays as separate anomally 
#anommalies that last longer period based on the sequential timestamp will be saved in one array
#Dataframe needs to have timestamp in the column 0 in datetime  %Y-%m-%d %H:%M:%S
def extract_annomalies(dataframe_anomalies,interval_minutes,output_dictionary,name ):
    anomalies_list_datetime=dataframe_anomalies.values.tolist()
   
    while len(anomalies_list_datetime)>0:
        for r in anomalies_list_datetime: 
            r=anomalies_list_datetime.index(r)
            
            if r==0:
                results=[]
                results.append(anomalies_list_datetime[r])
            elif r!=0 and (anomalies_list_datetime[r][2]-results[-1][2]).total_seconds()/60==interval_minutes: 
                results.append(anomalies_list_datetime[r])
        #change results timestamp to string 
        annomaly_list_string=[]
        for i in results: 
            i=results.index(i)
            annomaly_list_string.append([(results[i][2].strftime('%Y-%m-%d %H:%M:%S')),results[i][3]])
            #interval in minutes 
            if len(results)>1:
                duration=(len(results)-1)*interval_minutes
            else: 
                duration=1*interval_minutes
                
        #save to data dictionary 
        output_dictionary.append({
             'name': name,
             'duration': str(duration), 
             'anomalies_details': annomaly_list_string
               })
        anomalies_list_datetime = [x for x in anomalies_list_datetime if x not in results] 
    return [output_dictionary]