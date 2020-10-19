# -*- coding: utf-8 -*-
"""
Created on Fri Nov 29 16:17:17 2019

@author: ABachleda-Baca
"""
import pandas as pd
import numpy as np
import math
#Calculate global solar radiation from Kasten Czeplak model for global solar radiation on the horizontal surface under cloud cover conditions 
#Ig=Igc(1-a(cloud_cover/8)^b)
#a and b are defoult arguments they can be change for custom parameters 
def kasten_czeplak(
        clearsky_irradiance,
        cloud_cover_octas,
        a=0.75,
        b=3.4
        ):
    
    global_irradiance1=clearsky_irradiance*(1-a*((cloud_cover_octas/8)**b))
    return global_irradiance1
#Kasten model best fit
def kasten_czeplak_fit_supervisor(xdata, a, b):
    return kasten_czeplak(clearsky_irradiance = xdata[:, 0], cloud_cover_octas = xdata[:, 1], a = a, b = b)
#Calculate global solar radiation from Zhang Huang Solar model 
#I=[I0⋅sin(h)⋅(c0+c1⋅CC+c2⋅CC2+c3(Tn−Tn−3)+c4⋅φ+c5⋅Vw)+d]k
def zhang_huang(
        solar_altitude,
        cloud_cover,
        temperature_deg,
        temp_n_min3,
        relhumidity,
        wind_speed,
        solar_constant=1355,
        c0=0.5598,
        c1=0.4982,
        c2=-0.6762,
        c3=0.02842,
        c4=-0.00317,
        c5=0.014,
        d=-17.853,
        k=0.843
        ):
    
    # Convert degrees to radians
    if solar_altitude.min() < -10 or solar_altitude.max() > 10:
        solar_altitude_rad = solar_altitude * math.pi / 90
    else:
        solar_altitude_rad = solar_altitude
    
    global_irradiance2=(solar_constant * np.sin(solar_altitude_rad) * (c0 + (c1 * cloud_cover) + (c2 * (cloud_cover**2)) + (c3 * (temperature_deg - temp_n_min3)) + (c4 * relhumidity) + (c5 * wind_speed)) + d) / k
    
    global_irradiance2[global_irradiance2 < 0] = 0
    
    return global_irradiance2

def zhang_huang_fit_supervisor(xdata, c0, c1, c2, c3, c4, c5, d, k):
    return zhang_huang(
                solar_altitude = xdata[:, 0],
                cloud_cover = xdata[:, 1],
                temperature_deg = xdata[:, 2],
                temp_n_min3 = xdata[:, 3],
                relhumidity = xdata[:, 4],
                wind_speed = xdata[:, 5],
                solar_constant=1355,
                c0=c0,
                c1=c1,
                c2=c2,
                c3=c3,
                c4=c4,
                c5=c5,
                d=d,
                k=k
        )
    