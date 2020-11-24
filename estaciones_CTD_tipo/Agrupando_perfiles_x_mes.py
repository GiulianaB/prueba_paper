"""
Rutina para agrupar mensualmente los perfiles.
1. Lista todos los perfiles dentro de la carpeta
"""

# path_gral = '/home/daniu/Documentos/'
path_gral = '/media/giuliana/Disco1TB/'

#Librerias
import os
import pandas as pd
from datetime import datetime
import numpy as np
import pickle

#Funciones:
def promedio_mensual_datos(path_files,files_mes):
    """
    Promedia los perfiles que se encuentran en files_mes dentro del path_files

    INPUTS
    path_files: str.
        path donde se encuentran los files_mes
    files_mes: array
        array con los nombres de los archivos que quiero promediar los perfiles.

    OUTPUTS
    df: DataFrame
        dataframe con los datos de los perfiles asociados a ese mes. Se promedia
        las variables prof a prof.
        keys: 'PRES', 'SAL','TEMP'.
    """
    import pickle
    import numpy as np
    cant_files = len(files_mes)
    P_mes, S_mes, T_mes = np.nan*np.ones((5001,cant_files)),np.nan*np.ones((5001,cant_files)),np.nan*np.ones((5001,cant_files))
    for count,f in enumerate(files_mes):
        perfil = pickle.load(open(path_gral + path_files + f , 'rb'))
        if count == 0: P = perfil['data']['PRES']
        S_mes[:,count] = perfil['data']['SAL']
        T_mes[:,count] = perfil['data']['TEMP']

    # Datos promediados mensual
    d = {'PRES': P,
         'SAL' : np.nanmean(S_mes, axis = 1),
         'TEMP': np.nanmean(T_mes, axis = 1 )}
    df = pd.DataFrame(data = d)


    return df
##############################################################
caja = 'sur'
path_files = 'prueba_paper/estaciones_CTD_tipo/Box_'+str(caja)+'/'
files = os.listdir(path_gral + path_files)

# lista de fechas asociadas a los files
fechas = [i.split('_',3)[-1] [:-2] for i in files]
fechas_dt = pd.to_datetime([datetime.strptime(i, '%d%m%Y') for i in fechas])

# Tiempo
Y_inicial, Y_final = 1978, 2018
m_inicial, m_final = '01', '12'
time = pd.date_range(start = str(Y_inicial)+str(m_inicial)+'01', end = str(Y_final)+str(m_final) +'01', freq = 'M')

for yyyy in range(Y_inicial, Y_final+1):
    for mm in range(int(m_inicial),int(m_final)):
        fecha = datetime.strptime(str(yyyy)+str(mm), '%Y%m')
        mask = np.logical_and(fechas_dt.month == mm, fechas_dt.year == yyyy )
        files_mes = np.array(files)[mask]
        if len(files_mes) != 0:
            df = promedio_mensual_datos(path_files,files_mes)
            p = {'time': fecha,
                'caja': caja,
                 'data': df}
            pickle.dump(p, open(path_gral + path_files[:-1] + '_mensual/'+str(fecha)+'.p', "wb" ) )





##
