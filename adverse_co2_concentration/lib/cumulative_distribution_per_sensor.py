# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 11:44:32 2020

@author: agnieszka
"""



import matplotlib.pyplot as plt


def cumulative_distribution_per_sensor(figure_size,sensors_with_anomalies,data,destination_path,upper_bound):
    
    total_anomalies=[]  
    for sensor_name in sensors_with_anomalies:
        x=[]
        for i in (data['anomalies']['anomaly_co2_values'][sensor_name][0]):
            i=data['anomalies']['anomaly_co2_values'][sensor_name][0].index(i)
            #save all the duration to the array 
            x.append(round((float(data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['duration'])/60.00),2))
            total_anomalies.append(round((float(data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['duration'])/60),2))
            #assign 1 to event ass in that situation event always occure 
        summary_anomalies=round(sum(x),2)
        plt.figure(figsize=figure_size) 
    
     
        n, bins, patches = plt.hist(x, density=True, histtype='step',
                           cumulative=True, label=sensor_name)
        plt.suptitle('Cumulative distribution for periods recorded when CO2 level higher than '+str(upper_bound)+'\n Total period of time with adverse conditions: ' +str(summary_anomalies)+  'hr', fontsize=15)
        plt.ylim(ymax = 1.5, ymin = 0.0)
        plt.legend(fontsize=15, loc='upper left')
        plt.xlabel('duration of anomaly[hours]')
        plt.ylabel('relative amount')
        plt.savefig(destination_path+sensor_name+'.png') 
        plt.show()