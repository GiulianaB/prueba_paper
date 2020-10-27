"""
Rutina para acomodar los perfiles de la caja Norte

Dani Risaro
Giuli Berden
"""
# path_gral = '/home/daniu/Documentos/'
path_gral = '/media/giuliana/Disco1TB/'

#Librerias
import pickle
import pandas as pd
import numpy as np


# Funciones#########################################
def detecta_salto(a):
    """
    Detecta si hay dos estaciones con el mismo nombre. El criterio es la ubicacion,
    si existen dos mediciones con un mismo nombre y ubicacion (latitud y longitud)
    diferentes, son estaciones diferentes. y por fechas.

    INPUTS
    ------
    a: list
        lista de indices de la estacion
    OUTPUTS
    ------
    salto: np.nan or int
        Si existe un salto, salto == indice del inicio de las estaciones.
        Si no hay salto, salto == np.nan.
    """

    return salto
###################################################

path = path_gral + 'prueba_paper/estaciones_CTD_tipo/BoxNorte_NivelesStd.csv'

data_box_norte = pd.read_csv(path)

# 1. Listar las estaciones
lista = list(data_box_norte['Nroest'])
estaciones = list(set([k for k in lista if lista.count(k)>=1]))

lista = np.array(lista)
estaciones_mismo_nombre = []
# Agrupo todas los datos con el mismo nombre de estacion
for est in estaciones:
    ind_est = np.where(lista == est)[0]
    d = {'est':est,
        'Lat': data_box_norte['Latitud'][ind_est],
        'Lon': data_box_norte['Longitud'][ind_est],
        'Fecha': data_box_norte['FechayHora'][ind_est],
        'Presion': data_box_norte['Presion'][ind_est],
        'Temperatura': data_box_norte['Temperatura'][ind_est],
        'Salinidad': data_box_norte['Salinidad'][ind_est]
        }
    df_est = pd.DataFrame(data = d)

    # Agrupo todos los datos con el mismo nombre de estacion y latitud.
    lista_latitudes = list(df_est['Lat'])
    latitudes = list(set([k for k in lista_latitudes if lista_latitudes.count(k)>=1]))
    for count_lat, lat0 in enumerate(latitudes):
        ind_est_lat = np.where(np.array(lista_latitudes) == lat0)[0]
        d = {'est':est,
            'Lat': lat0,
            'Lon': df_est['Lon'].values[ind_est_lat],
            'Fecha': df_est['Fecha'].values[ind_est_lat],
            'Presion': df_est['Presion'].values[ind_est_lat],
            'Temperatura': df_est['Temperatura'].values[ind_est_lat],
            'Salinidad': df_est['Salinidad'].values[ind_est_lat]
            }
        df_est_lat = pd.DataFrame(data = d)

        # Agrupo todos los datos con el mismo nombre de estacion, latitud y longitud.
        lista_longitudes = list(df_est_lat['Lon'])
        longitudes = list(set([k for k in lista_longitudes if lista_longitudes.count(k)>=1]))

        for count_lon, lon0 in enumerate(longitudes):
            ind_est_lat_lon = np.where(np.array(lista_longitudes) == lon0)[0]
            d = {'est':est,
                'Lat': lat0,
                'Lon': lon0,
                'Fecha': df_est_lat['Fecha'].values[ind_est_lat_lon],
                'Presion': df_est_lat['Presion'].values[ind_est_lat_lon],
                'Temperatura': df_est_lat['Temperatura'].values[ind_est_lat_lon],
                'Salinidad': df_est_lat['Salinidad'].values[ind_est_lat_lon]
                }
            df_est_lat_lon = pd.DataFrame(data = d)

            # Agrupo todos los datos con el mismo nombre de estacion, latitud, longitud y fecha.
            lista_fechas = list(df_est_lat_lon['Fecha'])
            lista_fechas_sin_horas = []
            for f in lista_fechas:
                lista_fechas_sin_horas.append(f[0:11])
            fechas = list(set([k for k in lista_fechas_sin_horas if lista_fechas_sin_horas.count(k)>=1]))
            for count_fecha, fecha0 in enumerate(fechas):
                ind_est_lat_lon_fecha = np.where(np.array(lista_fechas_sin_horas) == fecha0)[0]
                # Ordeno por presion:
                P = df_est_lat_lon['Presion'].values[ind_est_lat_lon_fecha]
                S = df_est_lat_lon['Salinidad'].values[ind_est_lat_lon_fecha]
                T = df_est_lat_lon['Temperatura'].values[ind_est_lat_lon_fecha]
                data = np.nan*np.ones((len(P),3))
                data[:,0],data[:,1],data[:,2] = P,S,T
                data_sort = data[data[:,0].argsort()]

                # Datos
                d = {'PRES': data_sort[:,0],
                     'SAL' : data_sort[:,1],
                     'TEMP': data_sort[:,2]}
                df = pd.DataFrame(data = d)
                if np.max(np.abs(d['TEMP'])) >30:
                    print('Temp >30grad, estacion:',est)

                nombre = 'bn' +str(est)+'_'+str(count_lat)+'_'+str(count_lon)+'_'+str(count_fecha)
                dic = {'estacion':nombre,
                    'fecha': fecha0,
                    'lat': lat0,
                    'lon': lon0,
                    'data': df}

                pickle.dump(dic, open(path_gral + 'prueba_paper/estaciones_CTD_tipo/Box_norte/'+str(nombre)+'.p', "wb" ) )

















##
