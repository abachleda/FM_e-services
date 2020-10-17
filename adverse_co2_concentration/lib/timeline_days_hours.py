# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 12:29:14 2020

@author: agnieszka
"""
import pandas as pd
import math
from bokeh.plotting import figure, output_file, save, show
from bokeh.io import export_png
from bokeh.models  import FixedTicker, LinearAxis
import numpy as np
#This function will draw a timeline graph  including all recorded anomalies previously stored in data dictionary 

def timeline_days_hours(interval_frequency,all_co2_dataframe,sensors_with_anomalies,data,upper_bound,destination_path):
    times = pd.date_range(start='00:00:00', end='23:55:00', freq=str(interval_frequency)+'Min').strftime('%H:%M:%S')
    days= all_co2_dataframe['timestamp'].dt.strftime('%Y-%m-%d').to_list()
    days = list(dict.fromkeys(days))
    timestamp=list(times)
    for sensor_name in sensors_with_anomalies:
        all_durations=[]
        for k in data['anomalies']['anomaly_co2_values'][sensor_name][0]:
            k=data['anomalies']['anomaly_co2_values'][sensor_name][0].index(k)
            all_durations.append(int(data['anomalies']['anomaly_co2_values'][sensor_name][0][k]['duration']))
        data['anomalies']['anomaly_co2_values'][sensor_name][0]
        p=figure(plot_height=500,
                 plot_width=2000,
                 x_range=timestamp,
                 y_range=days,
                 title='Timeline of periods with CO2 levels higher than '+str(upper_bound)+' ppm in '+sensor_name+'\n Based on data for last '+str(len(days))+' days',
                 active_drag = None,
                 toolbar_location=None)
        p.x_range.range_padding = 0
        p.y_range.range_padding = 0
        p.title.text_font_size = '15pt'
        p.xaxis.axis_label_text_font_size = "15pt"
        p.yaxis.axis_label_text_font_size = "15pt"
        p.yaxis.major_label_text_font_size='9pt'
        p.xaxis.major_label_text_font_size='5pt'
        # set x axis to invisible 
        p.xaxis.visible = False
        # Add custom axis with tickers labels only every 1 hour
        labels= np.arange(0, 288, 12).tolist()
        ticker = FixedTicker()
        ticker.ticks = labels
        xaxis = LinearAxis(ticker=ticker)
        xaxis.major_label_orientation = math.pi/3
        p.add_layout(xaxis, 'below')
        
        xaxis.major_label_overrides = {0: '00:00', 12: '01:00',24: '02:00', 36:'3:00', 48: '04:00', 60: '05:00', 72: '06:00', 84:'07:00', 96: '08:00', 108:'09:00', 120: '10:00', 132: '11:00', 144: '12:00', 156: '13:00',
                                        168: '14:00', 180: '15:00', 192: '16:00', 204: '17:00', 216: '18:00', 228: '19:00', 240: '20:00', 252: '21:00', 264: '22:00', 276: '23:00'}
        #add anomalies recorded for each day in considered period 
        for i in  data['anomalies']['anomaly_co2_values'][sensor_name][0]:
            i=data['anomalies']['anomaly_co2_values'][sensor_name][0].index(i)
            x=[]
            y =[]
            x.append(data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['anomalies_details'][0][0][11:])
            x.append(data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['anomalies_details'][-1][0][11:])
            y.append(data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['anomalies_details'][0][0][0:10])
            y.append(data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['anomalies_details'][-1][0][0:10])
            if data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['anomalies_details'][0][0][0:10]==data['anomalies']['anomaly_co2_values'][sensor_name][0][i]['anomalies_details'][-1][0][0:10]:
               # print('yes')
               p.line(x,y, line_width=2,color='blue', legend_label = 'CO2 above critical value')
               p.circle(x, y, fill_color="blue", line_color='blue', size=5)
            else: 
                x1=x.copy()
                y1=y.copy()
                x2=x.copy()
                y2=y.copy()
                x1[-1]=times[-1]
                y1[-1]=y1[0]
                p.line(x1,y1, line_width=2,color='blue')
                x2[0]=times[0]
                y2[0]=y2[-1]
                p.line(x2,y2, line_width=2,color='blue')
                x3=[x1[0],x2[-1]]
                y3=[y1[0],y2[-1]]
                p.circle(x3,y3, fill_color="blue", line_color='blue', size=5)
        
        #save graph in output location 
        output_file(destination_path+'/anomalies_timeline_'+sensor_name+'.html')
        save(p)
    return p 