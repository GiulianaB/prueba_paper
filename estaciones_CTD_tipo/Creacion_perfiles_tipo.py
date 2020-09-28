#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 18:03:00 2020

Perfiles CTD para probar en .csv
@author: giuliana
"""
from seabird import fCNV
import pandas as pd


files = ['d01.cnv','d02.cnv','d040.cnv','d050.cnv']
for f in files:
    
    CTD1 = fCNV(f)

    d = {'LAT' : CTD1['LATITUDE'],
         'LON' : CTD1['LONGITUDE'],
         'PRES': CTD1['PRES'],
         'SAL' : CTD1['PSAL'],
         'TEMP': CTD1['TEMP']}
    df = pd.DataFrame(data = d)
    df.to_csv(f[:3]+'.csv')
    

