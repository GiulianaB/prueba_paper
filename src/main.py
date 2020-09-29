"""
En esta rutina vamos a generar los cálculos para el mejor paper

Dani Risaro
Giuli Berden
"""

import sys
sys.path.append('/home/daniu/Documentos/prueba_paper/src')

import aux

# leemos perfil
path = '/home/daniu/Documentos/prueba_paper/estaciones_CTD_tipo/'
filename = 'd01.p'

df, lat, lon, fecha = aux.read_pickle(path + filename)

# 3. estratificación
# TODO - parametro de simpson
# TODO - profundidad de la capa de mezcla

# TODO - generar columna con densidad potencial

# 1. Climatologia a diferentes niveles (a definir)
# TODO - para esto necesitariamos trabajar con varios perfiles a la vez

# 2. variabilidad interanual de T y S,
# TODO - para esto necesitariamos trabajar con varios perfiles a la vez
