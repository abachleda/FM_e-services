
# File manipulation
import sys
import os
sys.path.append('C:/FM_e-services-main/submeters_energy_share')
os.chdir('C:/FM_e-services-main/submeters_energy_share')


# Misc
import pandas as pd
import psycopg2

from fpdf import FPDF
from datetime import datetime, timedelta

#chart libraries 
from math import pi
from bokeh.palettes import Category10
from bokeh.models.sources import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import cumsum 
from bokeh.models import Legend, HoverTool, LabelSet, LegendItem
from bokeh.io import output_notebook, show, push_notebook
from bokeh.io import export_png
from bokeh.transform import factor_cmap
from bokeh.plotting import figure, save, output_file
from bokeh.palettes import *
import numpy as np
import json


# Custom functions

from lib.send_email import send_email



###SERVICE CONFIGURATION####
#Specify submeters that you want to include in report 

meters=['Heating pumps','Small Power','Kitchens','IT Communications','Workshops','Auditoriums','Mechanical Plant',
            'Lifts','Labs','Chillers','Fume Cupboard Extracts','Lighting','AHUs','HM-TI-01']



#define considered period in days 
period=7

recipient_email='<provide_recipient_email>'

building_name='Test_Building_01'
###########################################################


#import data from the file 
energy_summary = pd.read_csv('data/energy_data.csv') 
energy_summary= energy_summary[['timestamp','energy_kwh','meter']]
energy_summary.timestamp= pd.to_datetime(energy_summary.timestamp)
#sort vales by timestamp
energy_summary=energy_summary.sort_values(by=['timestamp'])

end_date= energy_summary['timestamp'].iloc[-1]
start_date=end_date- timedelta (days=period)

#choose the period of 7 days 
mask = (energy_summary['timestamp'] >= start_date) & (energy_summary['timestamp'] <= end_date)
energy_summary= energy_summary.loc[mask]
#choose values only for considered submeters 
energy_summary=energy_summary.loc[energy_summary['meter'].isin(meters)]

#reset index
energy_summary.reset_index(inplace=True)
del energy_summary['index']
#put every meter in separate column 

energy_summary = energy_summary.pivot_table(index='timestamp',columns='meter')
#change name for the heating meter to more user friendly 
energy_summary.rename(columns={'HM-TI-01':'Total district heating'},inplace=True)
#change index to datetime 
energy_summary.index= pd.to_datetime(energy_summary.index)

#define new dataframe to put values of weekly energy usage in it 
weekly_summary_consumption = pd.DataFrame()
#weekly summary for each meter 
weekly_summary_consumption = energy_summary.resample('168H').sum().round(decimals=0)
#change name of the columns 
weekly_summary_consumption.columns=[str(s2) for (s1,s2)in weekly_summary_consumption.columns.tolist()]
#remove index name
weekly_summary_consumption.index.name=None
#reset index 
weekly_summary_consumption.reset_index(inplace=True)
#change name of column index to timestamp 
weekly_summary_consumption=weekly_summary_consumption.rename({'index':'timestamp'},axis=1)
#put all meters in the same column 
weekly_summary_consumption=pd.melt(weekly_summary_consumption,id_vars='timestamp',var_name='Meter',value_name='energy_kwh')
#calculate total energy from all meters 
total_energy_consumption= weekly_summary_consumption.energy_kwh.sum().round(decimals=0)

# Take into account values that are bigger than 0 for graph
weekly_summary_consumption_graph = weekly_summary_consumption[weekly_summary_consumption['energy_kwh'].round(decimals=0) > 0]

# calculate contribution of every meter in total energy usage in % rounded to 1 decimal point 
weekly_summary_consumption['energy_contribution']= (weekly_summary_consumption['energy_kwh']/total_energy_consumption*100).round(decimals=0)
weekly_summary_consumption=weekly_summary_consumption.sort_values(by='energy_contribution', ascending=False)
weekly_summary_consumption.reset_index(inplace=True)
weekly_summary_consumption_graph = weekly_summary_consumption[weekly_summary_consumption['energy_contribution'].round(decimals=0) > 0]
#sort values by energy usage contribution 
weekly_summary_consumption_graph=weekly_summary_consumption_graph.sort_values(by='energy_contribution', ascending=False)

#convert dataframe columns to dictionary
submeters_dict={}
submeters_dict.update({'timestamp':end_date.strftime('%Y-%m-%d %H:%M:%S')})
submeters_dict.update({'period_days': period})
submeters=dict(zip(weekly_summary_consumption_graph.Meter, weekly_summary_consumption_graph.energy_contribution))
submeters_dict.update(submeters)

report_date= end_date.strftime('%Y-%m-%d')
##save the results in service output 

with open('output/'+report_date+'.json', 'w') as fp:
    json.dump(submeters_dict, fp)

colors=['#8B008B','#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
        '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f', '#c7c7c7', '#bcbd22', '#dbdb8d', '#17becf', '#9edae5','#4B0082']


# libraries

import matplotlib.pyplot as plt
import squarify    # pip install squarify (algorithm for treemap)
import matplotlib.patches as mpatches 

fig, ax = plt.subplots()
squarify.plot(sizes=weekly_summary_consumption_graph['energy_kwh'].values, label=weekly_summary_consumption_graph['energy_contribution'].values, alpha=.8,color=colors,text_kwargs={'fontsize':17})
plt.axis('off')
all_patches=[]
for i in list(submeters.keys()):
    i= list(submeters.keys()).index(i)
    all_patches.append(mpatches.Patch(color=colors[i], label=weekly_summary_consumption_graph['Meter'].values[i]))
plt.legend(handles=all_patches, loc='lower left', bbox_to_anchor=(0, -2.1),fontsize=30)
fig.set_size_inches(10,5)#
plt.suptitle('Energy consumption in '+building_name, fontsize=20)
plt.savefig('charts/plot_treemap.png',bbox_inches='tight',pad_inches=1)

#Generation of PDF Report 
pdf = FPDF()
pdf.add_page()
pdf.set_xy(0, 0)
pdf.set_font('arial', 'B', 12)
pdf.cell(60)
pdf.cell(75, 10, "Contribution of meters in total Energy usage in "+building_name, 0, 2, 'C')
pdf.set_font('arial', 'B', 10)
#extract begining of the week
start_week=energy_summary.index[0]
#change to string
start_week=datetime.strftime(start_week, '%Y-%m-%d %H:%M:%S')
start_week=start_week[:10]
#extract end of the week
stop_week=energy_summary.index[-1]
#change to string
stop_week=datetime.strftime(stop_week, '%Y-%m-%d %H:%M:%S')
stop_week=stop_week[:10]
pdf.cell(75, 10, "Report generated on: "+ datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 2, 'C')
pdf.cell(75, 10, "Week: From "+start_week+' to '+stop_week , 0, 2, 'C')
pdf.cell(90, 10, 'The table shows all submeters in the building listed in order of energy usage, from highest to lowest', 0, 2, 'C')
pdf.cell(-40)
pdf.set_font('arial', 'B', 10)
pdf.cell(80, 10, 'Meter', 1)
pdf.cell(40, 10, 'Energy Usage [kWh]', 1)
pdf.ln()
pdf.cell(10)
pdf.set_font('arial', '', 10)
for i in range(0, len(weekly_summary_consumption)):
    pdf.cell(80, 10, '%s' % (weekly_summary_consumption.Meter[i]), 1)
    pdf.cell(40, 10, '%s' % (weekly_summary_consumption.energy_kwh[i]), 1)
    pdf.ln()
    pdf.cell(10)
    #pdf.cell(-90)
pdf.cell(90, 10, " ", 0, 2, 'C')
pdf.cell(-25)
pdf.image('charts/plot_treemap.png', x = None, y = None, w = 200, h = 280, type = '', link = '')
pdf.output('output/reports/submetering_report_'+report_date+'.pdf', 'F')
#send an email 

content='Please find the weekly report including energy consumption in '+building_name+', highlighting specific areas of consumption'
send_email(
        content,
        receivers = recipient_email,
        subject = 'Energy consumption statistics for '+building_name,
        file_location = 'output/reports/submetering_report_'+report_date+'.pdf',
        file_name = 'submeters_report'
        )

