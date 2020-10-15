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
