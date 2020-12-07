# -*- coding: utf-8 -*-
"""
Created on Thu Feb 20 10:27:14 2020

@author: agnieszka
"""

# -*- coding: utf-8 -*-
"""

@author: agnieszka bachleda-baca 
"""
#json and pdf libraries
import os
from fpdf import FPDF
import math
#bokeh graph
from bokeh.io import show, output_file,save
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.transform import dodge
from bokeh.io import export_png
from bokeh.models import Legend
from datetime import datetime
from selenium.webdriver import Firefox, FirefoxOptions

#import custom modules 
from lib.misc.time_period_extract import time_period_extract
from lib.misc.import_events_from_json import import_events_from_json
from lib.misc.extract_alerts_from_events import extract_alerts_from_events

def generate_pdf(name,end_date, pr_days):
    #initialise web driver to export fraphs to png 
    options = FirefoxOptions()
    web_driver=Firefox(executable_path='C:/Users/ABachleda-Baca/AppData/Local/salabs_/WebDriverManager/gecko/v0.27.0/geckodriver-v0.27.0-win64/geckodriver.exe',options=options)
    #Define period to be considered using time_period function 
    week_times=time_period_extract(days=pr_days,end_date=end_date)

    #Import data from json files in known directory using json_import function and save all recorded alerts#in events array 
    path='output/Building1/'
    events=import_events_from_json(week_times,path)
    #transform events from json file to list of dictionaries
    total_list=[]
    if events:
        total_list=extract_alerts_from_events(events)


    #extract the timestamps for daily energy usage 
    if total_list: 
        timestamp_daily_energy_gen=[]
        energy_daily_modelled_dc=[]
        energy_daily_gen_ac=[]
    for i in total_list[-1]['daily_energy']:
        i=total_list[-1]['daily_energy'].index(i)
        timestamp_daily_energy_gen.append((total_list[-1]['daily_energy'][i][0])[:10])
        energy_daily_modelled_dc.append(total_list[-1]['daily_energy'][i][1])
        energy_daily_gen_ac.append(total_list[-1]['daily_energy'][i][2])

    #Draw graph Daily energy generation 
    #bokeh plot generation mix and DH performance indicator 

    #draw a graph 
    if not os.path.exists('output/'+name+'/charts/DCvsAC'):
        os.makedirs('output/'+name+'/charts/DCvsAC', mode=0o777)    
    output_file('output/'+name+'/charts/DCvsAC/energy_output'+end_date[:10]+'.html')
    data={'timestamps':timestamp_daily_energy_gen,
          'energy_DC_modelled':energy_daily_modelled_dc,
          'energy_ac_generated':energy_daily_gen_ac}

    source= ColumnDataSource(data=data)
    p = figure(x_range=timestamp_daily_energy_gen, plot_width=700,plot_height=600, title='Daily Energy Output',
           toolbar_location=None, tools="")
    p.title.text_font_size = '15pt'
    p.xaxis.axis_label_text_font_size = "15pt"
    p.yaxis.axis_label_text_font_size = "15pt"
    p.yaxis.major_label_text_font_size='15pt'
    p.xaxis.major_label_text_font_size='12pt'
    p.yaxis.axis_label = 'Energy output [kWh]'
    a1=p.vbar(x=dodge('timestamps',0.0,range=p.x_range), top='energy_DC_modelled',width=0.25,source=source,color='#718dbf')
    a2=p.vbar(x=dodge('timestamps',0.25,range=p.x_range), top='energy_ac_generated',width=0.25,source=source,color='#00008B') 
    p.xgrid.grid_line_color = None
    legend = Legend(items=[
            ("Modelled Energy DC ",   [a1]),
            ("Measured Energy AC", [a2])
            ], location=(0, -5))

    p.add_layout(legend, 'below')
    p.y_range.start = 0
    save(p)  
    export_png(p, filename='output/'+name+'/charts/DCvsAC/energy_output'+end_date[:10]+'.png',webdriver=web_driver)

    #Extract PR for last 3 month 
    system_pr=[]
    timestamp_pr=[]
    for i in total_list:
        i=total_list.index(i)
        system_pr.append(total_list[i]['system_pr'])
        timestamp_pr.append(total_list[i]['timestamp'][:10])
    #Draw a graph 
    if system_pr: 
        #create directory for graph 
        if not os.path.exists('output/'+name+'/charts/PR'):
            os.makedirs('output/'+name+'/charts/PR', mode=0o777)
        #create directory for report
        if not os.path.exists('output/'+name+'/charts/reports'):
            os.makedirs('output/'+name+'/charts/reports', mode=0o777)
        output_file('output/'+name+'/charts/PR/pr_'+end_date[:10]+'.html')
        #draw graph to compare real energy output and predicted one 
        p=figure(plot_height=600,plot_width=1000,title="PR for past 3 months measured in weekly basis",x_range=timestamp_pr,y_range=(min(system_pr)-0.4, max(system_pr)+0.4))
        p.title.text_font_size = '15pt'
        p.xaxis.axis_label_text_font_size = "15pt"
        p.yaxis.axis_label_text_font_size = "15pt"
        p.yaxis.major_label_text_font_size='15pt'
        p.xaxis.major_label_text_font_size='15pt'
        p.xaxis.major_label_orientation = math.pi/2
        p.yaxis.axis_label = 'performance in decimals'
        p.line(timestamp_pr,system_pr, line_width=2,color='blue', legend_label = 'PR')
        p.circle(timestamp_pr, system_pr, size=10, color='red', alpha=0.5)
        save(p)
        export_png(p, filename='output/'+name+'/charts/PR/pr_'+end_date[:10]+'.png',webdriver=web_driver)

        #Generation of PDF Report 
        pdf = FPDF()
        pdf.add_page()
        pdf.set_xy(0, 0)
        pdf.set_font('arial', 'B', 12)
        pdf.cell(60)
        pdf.cell(75, 10, "Performance of PV System in "+name, 0, 2, 'C')
        pdf.set_font('arial', 'B', 10)
        #extract begining of the week
        #change to string
       
        start_day=timestamp_pr[-2]
        stop_day=timestamp_pr[-1]
        pdf.cell(75, 10, "Report generated on: "+ datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 2, 'C')
        pdf.cell(75, 10, "Week: From "+start_day+' to '+stop_day , 0, 2, 'C')
        pdf.cell(ln=1, h=5.0, w=0, border=0)
        pdf.cell(60)
        pdf.set_font('arial', '', 10)
        pdf.cell(-60)
        pdf.cell(90, 10, 'Total calculated nominal energy output from PV array(DC Energy): '+str(total_list[-1]['total_energy_modelled_dc'])+' kWh', 0, 2, 'L')
        pdf.cell(90, 10, 'Total energy generated from PV system (AC Energy): '+str(total_list[-1]['total_energy_generated_ac'])+' kWh', 0, 2, 'L')
        pdf.cell(90, 10, 'Performance ratio of the PV System , calculated as:', 0, 2, 'L')
        pdf.cell(90, 10, 'Total energy generated from PV system/Total calculated nominal energy output from PV array: PR= '+str(total_list[-1]['system_pr']), 0, 2, 'L')
        pdf.cell(90, 10, 'Total calculated losses of the system  : '+str(round(((1-total_list[-1]['system_pr'])*100),2))+'%', 0, 2, 'L')
        pdf.cell(10)
        pdf.cell(ln=1, h=5.0, w=0, border=0)
        pdf.cell(ln=1, h=5.0, w=0, border=0)
        pdf.cell(ln=1, h=5.0, w=0, border=0)
        pdf.image('output/'+name+'/charts/DCvsAC/energy_output'+end_date[:10]+'.png', x = None, y = None, w = 150, h = 120, type = '', link = '')
        pdf.cell(ln=1, h=5.0, w=0, border=0)
        pdf.image('output/'+name+'/charts/PR/pr_'+end_date[:10]+'.png', x = None, y = None, w = 170, h = 100, type = '', link = '')
        pdf.set_font('arial', 'B', 10)
        pdf_report_location='output/'+name+'/charts/reports/Pv_performance'+end_date[:10]+'.pdf'
        pdf.output(pdf_report_location, 'F')
    
        return pdf_report_location