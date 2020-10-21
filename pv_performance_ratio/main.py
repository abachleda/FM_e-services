import os
import sys
# define the base directory 
sys.path.append('C:/KTP_e-services-master/pv_performance_ratio')
os.chdir('C:/KTP_e-services-master/pv_performance_ratio')
import pandas as pd
import numpy as np
import json
import pvlib
from datetime import datetime,timedelta
from pvlib import  tools

#custom functions 

from lib.ghi_models import kasten_czeplak
from lib.ghi_models import zhang_huang
# Custom functions
from lib.write_to_alertlog_4par import write_to_alertlog_4par
from lib.generate_pdf import generate_pdf
from lib.send_email import send_email 
from timezonefinder import TimezoneFinder

#%% Service configuration 
#location parameters 
name='Glasgow-Building01'
latitude=55.513
longitude=-4.143
altitude=48
#Set whih empirical model use in calculations. The options are ghi_model : kasten, zhang-huang decomp-model: dirint, erbs 
ghi_model='kasten'
decomp_model='dirint'
#pvsystem parameters 
surface_tilt=10 
surface_azimuth= 157.5
active_area=572.26
efficiency_modules= 0.143
# number of days considered
interval=7
#number of days taken into account for PR visualisation 
pr_days=90
#%% Modeling of sollar irradiance 
#load the data 
weather_data=pd.read_csv('data/weather_data.csv').sort_values(by=['timestamp'])
energy_output_meter=pd.read_csv('data/generation_meter_readings.csv').sort_values(by=['timestamp'])



#save the dates=
end_date= (energy_output_meter['timestamp'].iloc[-1])
start_date=pd.to_datetime(end_date)- timedelta (days=interval-1)
#change date back to string 
start_date=start_date.strftime("%Y-%m-%d %H:%M:%S")[:10]+' 00:00:00'
#save present date for report 
#present_date=datetime.today().strftime('%Y-%m-%d %H:%M:%S')
#present_day=datetime.today().strftime('%Y-%m-%d %H:%M:%S')[:10]


#%%5 modelling of clear sky irradiation https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.clearsky.ineichen.html?highlight=ineichen

#time range for model  Reference: 
tzf = TimezoneFinder(in_memory=True)
tz = tzf.timezone_at(lng = longitude, lat = latitude)
times = pd.date_range(start=start_date, end=end_date, freq='30Min', tz=tz)
pressure = pvlib.atmosphere.alt2pres(altitude)
solpos = pvlib.solarposition.get_solarposition(times, latitude, longitude,altitude,pressure)
apparent_zenith = solpos['apparent_zenith']
airmass_relative = pvlib.atmosphere.get_relative_airmass(apparent_zenith)
airmass_absolute = pvlib.atmosphere.get_absolute_airmass(airmass_relative, pressure)
linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(times, latitude, longitude)
dni_extra = pvlib.irradiance.get_extra_radiation(times)
#calculates ghi,dhi and dni and the results is a dataframe 
ineichen = pvlib.clearsky.ineichen(apparent_zenith, airmass_absolute, linke_turbidity, altitude, dni_extra)
#convert to utc timezone as the weather station data is in UTC time zone 
#ineichen = ineichen.tz_convert("UTC")
#reset index 
ineichen.reset_index(inplace=True)
ineichen= ineichen.rename(columns={'index': "timestamp",'ghi':'ghi_perez','dni':'dni_perez','dhi':'dhi_perez'})

#format weather data 
weather_data['timestamp']=pd.to_datetime(weather_data['timestamp'])
weather_data=weather_data.set_index('timestamp')
weather_data = weather_data.tz_localize("Europe/London")
weather_data.reset_index(inplace=True)

#%% merge weather data and modeled ghi into one dataframe and add some more columns 
irradiance=pd.merge(ineichen,weather_data, on='timestamp') 
#order values by timestamp 
irradiance.sort_values(by=['timestamp'])
#add the solpos and dni_extra columns to irradiance dataframe 
solpos.reset_index(inplace=True)
solpos=solpos.rename(columns={'index': "timestamp"})
irradiance=pd.merge(irradiance,solpos, on='timestamp')
irradiance['timestamp']=pd.to_datetime(irradiance['timestamp'])
dni_extra=dni_extra.to_frame()
dni_extra = dni_extra.tz_convert("UTC")
dni_extra.reset_index(inplace=True)
dni_extra=dni_extra.rename(columns={'index': "timestamp",0:'dni_extra'})
irradiance=pd.merge(irradiance,dni_extra, on='timestamp')
#%%MODELING OF IRRADIANCE IN THE CLOUDY CONDITION 
# Add columns with the right values needed for model 
irradiance['cloud_cover_octas'] = irradiance['clouds']*8/100
irradiance['cloud_cover_fraction']=irradiance['clouds']/100
#change temperature to celcius degrees 
irradiance['temperature']=irradiance['temperature']-273.15 
irradiance['temp_n_min3'] = irradiance['temperature'].shift(periods = -3, axis = 0).fillna(irradiance.loc[irradiance.index[irradiance.shape[0] - 1], 'temperature'])
irradiance['pressure_Pa']=irradiance['pressure']*100
#Calculate ghi : Kasten and zhang-huang models 
#provide arguments: cloud cover, clearsky_irradiance optional:a,b (taken from the optimisation model for glasgow)
irradiance['ghi_kasten']=kasten_czeplak(a=0.649,b=2.743,cloud_cover_octas=irradiance['cloud_cover_octas'],clearsky_irradiance=irradiance['ghi_perez'])
irradiance['ghi_kasten']=irradiance['ghi_kasten']
irradiance['ghi_kasten']=irradiance['ghi_kasten'].clip(lower=0)
#provide arguments: solar altitute,cloud cover, temperature_deg, 
irradiance['ghi_zhang']=zhang_huang(c0=226.902,c1=28.623,c2=-68.374,c3=1.310,c4=-1.575,c5=0.5669,d=-17391,k=278.113,solar_altitude=irradiance['elevation'],cloud_cover=irradiance['cloud_cover_fraction'],temperature_deg=irradiance['temperature'],relhumidity=irradiance['humidity'],wind_speed=irradiance['wind_speed'],temp_n_min3=irradiance['temp_n_min3'])  
#%%POA IRRADIANCE MODELLING####
#Refference https://www.osti.gov/pages/servlets/purl/1235343
##DECOMPOSITION MODEL DIRINT , ERBS 
#DIRINT 
#convert timestamp to index, because times values needs to be an array 
irradiance= irradiance.set_index('timestamp') 
times=irradiance.index
#choose which ghi results put to the decomosition model[kasten,zhang_huang]

if ghi_model=='kasten':
    ghi=irradiance['ghi_kasten']
elif ghi_model=='zhang_huang':
    ghi=irradiance['ghi_zhang']
    
#change solar_zenith to array values 
solar_zenith=irradiance['zenith']
pressure=irradiance['pressure_Pa']
dni_extra=irradiance['dni_extra']
#%%DECOMPOSITION MODEL [dirint,erbs]
#References: https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.irradiance.dirint.html
#https://pvlib-python.readthedocs.io/en/stable/generated/pvlib.irradiance.erbs.html
if decomp_model=='dirint':
    irradiance['dni']= pvlib.irradiance.dirint(
            ghi=ghi, 
            solar_zenith=irradiance['zenith'],
            times=irradiance.index, 
            pressure=irradiance['pressure_Pa'], 
            use_delta_kt_prime=True,
            temp_dew=None, 
            min_cos_zenith=0.065, 
            max_zenith=87)
    #replace nan with 0 
    irradiance['dni']=irradiance['dni'].fillna(0)
    #dhi from ghi=dni*cos(solar_zenith)+dhi
    cos_zenith = np.maximum(tools.cosd(solar_zenith), 0)
    irradiance['dhi'] = ghi - irradiance['dni']*cos_zenith
elif decomp_model=='erbs':
    erbs= pvlib.irradiance.erbs(
            ghi=ghi,
            solar_zenith=irradiance['zenith'], 
            datetime_or_doy=irradiance.index,
            min_cos_zenith=0.065, 
            max_zenith=87)
    irradiance=pd.merge(irradiance,erbs, on='timestamp') 
#%%TRANSPOSITION MODEL 
    #I_{tot} = I_{beam} + I_{sky diffuse} + I_{ground}
    #Hay-Davies for sky_diffuse
    #panel tilt from horizontal 
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      
    #surface azimuth depends on which side panels are facing
    #N=0 NNE=22.5 NE=45 ENE=67.5 E=90 ESE=110.5 SE=135 SSE=157.5 S=180 SSW=202.5 S=W=225 WSW=247.5 W=270 WNW=292.5 NW=315 NNW=337.5 
    #panel are facing SSE therefore: 
  
irradiance_total=pvlib.irradiance.get_total_irradiance(
            surface_tilt=surface_tilt, 
            surface_azimuth=surface_azimuth,
            solar_zenith=irradiance['zenith'], 
            solar_azimuth=irradiance['azimuth'], 
            ghi=ghi,
            dni=irradiance['dni'],
            dhi=irradiance['dhi'], 
            dni_extra=irradiance['dni_extra'],
            airmass=None,
            albedo=.25, 
            surface_type=None,
            model='haydavies')
#%% MODELLED ENERGY OUTPUT FROM ARRAY 
#join poa results to the irradiance dataframe 
irradiance=pd.merge(irradiance,irradiance_total, on='timestamp')
#reset index to draw the graph 
irradiance.reset_index(inplace=True)
irradiance['timestamp_str'] = irradiance.timestamp.dt.strftime('%Y-%m-%d %H:%M:%S')
#calculate the predicted energy output from PV panels (not taking into consideration losses of the system)  units [kWh]
irradiance['array_output']=(irradiance['poa_global']*active_area*efficiency_modules)/1000
#irradiance['predicted_energy']=
#%%EXPORT GENERATION METER DATA FROM DATABASE  
energy_output_meter=energy_output_meter[['meter','energy_kwh','timestamp']]
energy_output_meter=energy_output_meter[energy_output_meter['energy_kwh'].notnull()]
energy_output_meter=energy_output_meter.sort_values(by=['timestamp'])
energy_output_meter['timestamp']=pd.to_datetime(energy_output_meter['timestamp'])
#set timestamp as index 
energy_output_meter=energy_output_meter.set_index('timestamp')
energy_output_meter=energy_output_meter.tz_localize('UTC')
energy_output_meter=(energy_output_meter.resample('H').sum())
#merge energy generation data with irradiance datafram
irradiance=pd.merge(irradiance,energy_output_meter, on='timestamp')

   
#%% EXTRACT DAILY ENERGY GENERATED AC AND MODELLED DC 
irradiance_daily=irradiance[['timestamp', 'array_output','energy_kwh']] 
irradiance_daily=irradiance_daily.set_index('timestamp')
irradiance_daily=irradiance_daily.resample('D').sum()
irradiance_daily=irradiance_daily.reset_index()
irradiance_daily['timestamp']=irradiance_daily['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

#%% PERFORMANCE RATIO CALCULATIONS 
total_energy_modelled_dc=irradiance['array_output'].sum().round(decimals=1)
total_energy_generated_ac=irradiance['energy_kwh'].sum().round(decimals=1)
    
pr=(total_energy_generated_ac/total_energy_modelled_dc).round(decimals=2)
   
#%%DEFINE OUTPUTS
#%%define dictionary for output of the service 
data = {}
data['alerts'] = []

#create service output directory for location if doesn't exist 

if not os.path.exists('output/'+name):
    os.makedirs('output/'+name, mode=0o777)

#%%SAVE THE RESULTS IN THE DATA LOG AND JSON LOG 
#put the energy modelled dc and generated ac in the arrays  values 
daily_energy=irradiance_daily.round(decimals=1).values.tolist()
#save those to the data dictionary 
write_to_alertlog_4par(
        dictionary_to_append=data['alerts'],
        timestamp=end_date,message='PV System weekly output',
        details_name_par1='total_energy_modelled_dc',
        params1_list=total_energy_modelled_dc, 
        details_name_par2='total_energy_generated_ac',
        params2_list=total_energy_generated_ac,
        details_name_par3='system_pr',
        params3_list=pr,
        details_name_par4='daily_energy',
        params4_list=daily_energy)
#add pr to alerts log 
if data['alerts']: 
    #define the filename
    filename=end_date[:10]+'.json'
    #path to the outpu directory 
    file_path='outputs/'+name+'/'+filename
    # create a json file with data 
    with open(file_path,'w') as outfile: 
            json.dump(data, outfile)
            outfile.write('\n')
    
#%%generate pdf report and send emeil 
    pdf_report_location=generate_pdf(name=name,end_date=end_date,pr_days=pr_days)
      #send an email  
    send_email(
            content='Weekly energy performance report for PV system have been generated, please check the attachment',
            receivers = 'abachleda-baca@arbnco.com',
            #receivers = 'abachleda-baca@arbnco.com',
            subject = 'TIC- PV System performance report',
            file_location = pdf_report_location,
            file_name = 'pv_performance_report'
            )



