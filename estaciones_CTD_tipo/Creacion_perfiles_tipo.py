#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:03:00 2020

Perfiles CTD para probar en .csv
@author: giuliana
"""
from seabird import fCNV
import pandas as pd
import pickle


files = ['d01.cnv','d02.cnv','d040.cnv','d050.cnv','u035.cnv']

for f in files:

    CTD1 = fCNV(f)
    nombre = f[:3]
    fecha = str(CTD1.attributes['datetime'])[:10] # 'anio-mes-dia'
    lon = CTD1['LONGITUDE'].data.mean()
    lat = CTD1['LATITUDE'].data.mean()

    d = {'PRES': CTD1['PRES'],
         'SAL' : CTD1['PSAL'],
         'TEMP': CTD1['TEMP']}

    df = pd.DataFrame(data = d)

    dic = {'estacion':nombre,
            'fecha': fecha,
            'lat':lat,
            'lon':lon,
            'data':df}

    pickle.dump(dic, open(nombre+'.p', "wb" ) )
