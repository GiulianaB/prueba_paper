"""
Rutina para acomodar los perfiles de la caja Sur

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
    Detecta si existe un salto en la lista que indica que hay mas de una estacion
    con el mismo nombre. Para ello,
    calcula la diferencia de los indices a cada dato. Si observa un salto de
    indice, te dice el lugar donde pasa eso.

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
    b=[]
    for i in range(len(a)-1):
        b.append(a[i+1]-a[i])

    ind_salto = np.where((np.array(b) > 1) == True)[0]
    if len(ind_salto) != 0:
        salto_aux = ind_salto+1
        salto = np.zeros(len(salto_aux)+1)
        salto [1:] = salto_aux
        salto = salto.astype(int)
    else:
        salto = np.nan
    return salto
###################################################

path = path_gral + 'prueba_paper/estaciones_CTD_tipo/BoxSur_NivelesStd.xlsx'
data_box_sur = pd.read_excel(path)

# 1. Listar las estaciones
lista = list(data_box_sur['Nroest'])
estaciones = list(set([k for k in lista if lista.count(k)>=1]))

# 2. Creo los perfiles .p por separado
    #  estaciones no duplicadas en nombre
lista = np.array(lista)
estaciones_mismo_nombre = []
for est in estaciones:
    ind_est = np.where(lista == est)[0]
    salto = detecta_salto(ind_est)
    if np.isnan(np.sum(salto)) == True:
        # Metada de la estacion
        nombre  = est
        lat     = np.nanmean(data_box_sur['Latitud'][ind_est])
        lon     = np.nanmean(data_box_sur['Longitud'][ind_est])
        aux   = str(data_box_sur['FechayHora'][ind_est[0]])
        fecha = aux[:2]+'-'+aux[3:5]+'-'+aux[6:8]

        # Data de la estacion
        d = {'PRES':  data_box_sur['Presion'][ind_est],
             'SAL' :  data_box_sur['Salinidad'][ind_est],
             'TEMP':  data_box_sur['Temperatura'][ind_est]}
        df = pd.DataFrame(data = d)
        # Diccionario
        dic = {'estacion':nombre,
                'fecha': fecha,
                'lat':lat,
                'lon':lon,
                'data':df}
        # Lo guardo
        pickle.dump(dic, open(path_gral + 'prueba_paper/estaciones_CTD_tipo/Box_sur/bs_'+str(nombre)+'.p', "wb" ) )
    else:
        estaciones_mismo_nombre.append(est)
        print('Estaciones con mismo nombre',est)

    # Estaciones diferentes con mismo nombre
for est in estaciones_mismo_nombre:
    # indices del excel con el numero de estacion:
    ind_est = np.where(lista == est)[0]
    # Busco las distintas estaciones con el mismo nombre.
    salto = detecta_salto(ind_est)      # Indices de donde empieza cada est.
    cant_estaciones_mismo_nombre = len(salto)
    #Itero por cada estacion con el mismo nombre
    for i_st in range(cant_estaciones_mismo_nombre):
        print(i_st)
        # indices en excel de la estacion
        if i_st == cant_estaciones_mismo_nombre-1:
            indices_estacion_en_excel = ind_est[salto[i_st]:]
        else:
            indices_estacion_en_excel = ind_est[salto[i_st]:salto[i_st+1]]
        # Defino el nuevo nombre para diferenciarlas
        nombre  = str(est) + '_' + str(i_st)
        lat     = np.nanmean(data_box_sur['Latitud'][indices_estacion_en_excel])
        lon     = np.nanmean(data_box_sur['Longitud'][indices_estacion_en_excel])
        aux   = str(data_box_sur['FechayHora'][indices_estacion_en_excel[0]])
        fecha = aux[:2]+'-'+aux[3:5]+'-'+aux[6:8]

        # Data de la estacion
        d = {'PRES':  data_box_sur['Presion'][indices_estacion_en_excel],
             'SAL' :  data_box_sur['Salinidad'][indices_estacion_en_excel],
             'TEMP':  data_box_sur['Temperatura'][indices_estacion_en_excel]}
        df = pd.DataFrame(data = d)
        # Diccionario
        dic = {'estacion':nombre,
                'fecha': fecha,
                'lat':lat,
                'lon':lon,
                'data':df}
        # Lo guardo
        pickle.dump(dic, open(path_gral + 'prueba_paper/estaciones_CTD_tipo/Box_sur/bs_'+str(nombre)+'.p', "wb" ) )

# # Chequeo
#
# path = '/media/giuliana/Disco1TB/prueba_paper/estaciones_CTD_tipo/Box_sur/bs_10.p'
# pickle_perfil = pickle.load(open(path, 'rb'))
# df = pickle_perfil['data']
# df



"""
Rutina para acomodar los perfiles de la caja sur.
Separa por nombre de estacion. Dsp separo por latitud, longitud y fecha.
si el perfil tiene la misma cant de datos de presion, temperatura y salinidad,
lo guardo como un .p en la carperta Box_sur

Dani Risaro
Giuli Berden
"""
# path_gral = '/home/daniu/Documentos/'
path_gral = '/media/giuliana/Disco1TB/'

#Librerias
import pickle
import pandas as pd
import numpy as np
from dateutil import parser

#####Funcion
def f_interpolar_1_dbar(df):
    """
    Interpola los datos de los perfiles verticales cada 1 dbar.

    INPUTS
    df: DataFrame. keys: ['PRES','SAL','TEMP']
        datos del perfil vertical

    OUTPUTS
    df_interpolado: DataFrame. keys: ['PRES','SAL','TEMP']
        Datos del perfil vertical interpolado cada 1 dbar

    """
    import numpy as np
    import pandas as pd

    x   = df['PRES']
    y_T = df['TEMP']
    y_S = df['SAL']

    max_valor = int(len(x)-1)
    x_vals = np.linspace(0,max_valor,max_valor + 1 , dtype = int)
    y_T_interp = np.interp(x_vals, x, y_T)
    y_S_interp = np.interp(x_vals, x, y_S)

    # Relleno con Nans hasta 5000 dbar
    P = np.nan*np.ones(5001)
    T = np.nan*np.ones(5001)
    S = np.nan*np.ones(5001)

    P[:max_valor+1] = x_vals
    T[:max_valor+1] = y_T_interp
    S[:max_valor+1] = y_S_interp

    d = {'PRES': P,
         'SAL' : S,
         'TEMP': T}
    df_interpolado = pd.DataFrame(data = d)

    return df_interpolado

#######

path = path_gral + 'prueba_paper/estaciones_CTD_tipo/BoxSur_NivelesStd.xlsx'

data_box_sur = pd.read_excel(path)

# 1. Listar las estaciones
lista = list(data_box_sur['Nroest'])
estaciones = list(set([k for k in lista if lista.count(k)>=1]))

lista = np.array(lista)
estaciones_mismo_nombre = []
# Agrupo todas los datos con el mismo nombre de estacion
for est in estaciones:
    ind_est = np.where(lista == est)[0]
    d = {'est':est,
        'Lat': data_box_sur['Latitud'][ind_est],
        'Lon': data_box_sur['Longitud'][ind_est],
        'Fecha': data_box_sur['FechayHora'][ind_est],
        'Presion': data_box_sur['Presion'][ind_est],
        'Temperatura': data_box_sur['Temperatura'][ind_est],
        'Salinidad': data_box_sur['Salinidad'][ind_est]
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
                f_cambio_formato = f.strftime("%d%m%Y")
                lista_fechas_sin_horas.append(f_cambio_formato)
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

                # Chequeo que todas las variables tengan la misma dimension
                npres, ntemp, nsal = len(d['PRES']),len(d['TEMP']),len(d['SAL'])
                if npres == ntemp and npres == nsal:

                    # Interpolacion cada 1 dbar
                    df = f_interpolar_1_dbar(df)
                    nombre = 'bs' +str(est)+'_'+str(count_lat)+'_'+str(count_lon)+'_'+str(fecha0)
                    dic = {'estacion':nombre,
                        'fecha': f,
                        'lat': lat0,
                        'lon': lon0,
                        'data': df}

                    pickle.dump(dic, open(path_gral + 'prueba_paper/estaciones_CTD_tipo/Box_sur/'+str(nombre)+'.p', "wb" ) )
                    print(est)




##
