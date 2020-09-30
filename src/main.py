"""
En esta rutina vamos a generar los cálculos para el mejor paper

Dani Risaro
Giuli Berden
"""
# path_gral = '/home/daniu/Documentos/'
path_gral = '/media/giuliana/Disco1TB/'

#Librerias
import sys
sys.path.append(path_gral + 'prueba_paper/src')
import aux

# leemos perfil
path = path_gral + 'prueba_paper/estaciones_CTD_tipo/'
filename = 'd01.p'

df, lat, lon, fecha = aux.read_pickle(filename)

# 3. estratificación.
# Columna con densidad potencial y lo guarda en la carpeta perfiles
df, lat, lon, fecha = aux.add_sigma_tita(filename)
# Agrego columna de profundidad y lo sobreescribe en la carpeta perfiles
df, lat, lon, fecha = aux.add_prof(filename)
# Agrego parametro de simpson y lo sobreescribe en la carpeta perfiles
df, lat, lon, fecha, par_sim = aux.add_simpson_parameter(filename)


# TODO - profundidad de la capa de mezcla

# Guardar con las modificaciones.

# 0. Armar las series de tiempo de diccionarios de la caja elegida.

# 1. Climatologia a diferentes niveles (a definir)
# TODO - para esto necesitariamos trabajar con varios perfiles a la vez

# 2. variabilidad interanual de T y S,
# TODO - para esto necesitariamos trabajar con varios perfiles a la vez
