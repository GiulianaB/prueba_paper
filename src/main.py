"""
En esta rutina vamos a generar los cálculos para el mejor paper

Dani Risaro
Giuli Berden
"""
# path_gral = '/home/daniu/Documentos/'
path_gral = '/media/giuliana/Disco1TB/'

# Librerias
import sys
import matplotlib.pyplot as plt
sys.path.append(path_gral + 'prueba_paper/src')
import aux

# leemos perfil
path = path_gral + 'prueba_paper/estaciones_CTD_tipo/'

filename = 'bn1128_0_0_08121989.p'
# filename = 'bn1090_1_0_04121993.p'




df, lat, lon, fecha = aux.read_pickle(filename)

# Estratificación.
# Se crea la columna con densidad potencial y lo guarda en la carpeta perfiles
df, lat, lon, fecha = aux.add_sigma_tita(filename)

# Se agrega la columna de profundidad y lo sobreescribe en la carpeta perfiles
df, lat, lon, fecha = aux.add_prof(filename)

# Se agrega parametro de Simpson y lo sobreescribe en la carpeta perfiles
df, lat, lon, fecha, par_sim = aux.add_simpson_parameter(filename)

# Cálculo de la profundidad de la capa de mezcla
# Primero pruebo con el criterio de la tesis de Valen
Zref = 10                   # m.
umbral = 0.07               # kg/m3

df, lat, lon, fecha, par_sim, pcm = aux.add_pcm_umbral_densidad(filename, Zref, umbral)

aux.profile_layout(df, lat, lon, fecha, par_sim, pcm)


# Guardar con las modificaciones.

# 0. Armar las series de tiempo de diccionarios de la caja elegida.

# 1. Climatologia a diferentes niveles (a definir)
# TODO - para esto necesitariamos trabajar con varios perfiles a la vez

# 2. variabilidad interanual de T y S,
# TODO - para esto necesitariamos trabajar con varios perfiles a la vez
