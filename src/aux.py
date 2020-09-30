"""
Funciones auxiliares de main.py


"""

def read_pickle(filename):
    """
    INPUTS
    filename: str.

    OUTPUTS
    df: dataframe con PRES, SAL, TEMP
    lat: float, latitud
    lon: float, longitud
    fecha: str, fecha en YYYY-MM-DD
    """
    import pickle

    pickle_perfil = pickle.load(open('../estaciones_CTD_tipo/' + filename, 'rb'))

    df_datos = pickle_perfil.get('data')
    lat = pickle_perfil.get('lat')
    lon = pickle_perfil.get('lon')
    fecha = pickle_perfil.get('fecha')

    return df_datos, lat, lon, fecha


def add_sigma_tita(filename):
    """
    Agrega una columna a df de dens-tita, 'DENS', y lo guarda en la carpeta
    /prueba_paper/perfiles/filename.
    Necesita tener el archivo pickle con:
    fecha, lat, lon, df['PRES','SAL','TEMP']

    INPUTS
    filename: str.

    OUTPUTS
    df: dataframe con PRES, SAL, TEMP, DENS
    lat: float, latitud
    lon: float, longitud
    fecha: str, fecha en YYYY-MM-DD
    """
    import gsw
    import pickle

    df, lat, lon, fecha = read_pickle(filename)
    df['DENS'] = gsw.density.sigma0(df['SAL'], df['TEMP'])+1000
    #guardo en carpeta perfiles
    dic = {'nombre':filename[:3],
    'fecha':fecha,
    'lat':lat,
    'lon':lon,
    'df':df}
    pickle.dump(dic, open('../perfiles/'+filename, "wb" ) )

    return df, lat, lon, fecha


def read_pickle_perfiles(filename):
    """
    INPUTS
    filename: str.

    OUTPUTS
    df: dataframe con PRES, SAL, TEMP
    lat: float, latitud
    lon: float, longitud
    fecha: str, fecha en YYYY-MM-DD
    """
    import pickle
    import numpy as np

    pickle_perfil = pickle.load(open('../perfiles/' + filename, 'rb'))

    df_datos = pickle_perfil['df']
    lat = pickle_perfil.get('lat')
    lon = pickle_perfil.get('lon')
    fecha = pickle_perfil.get('fecha')

    if 'simp' in pickle_perfil.keys():
        par_sim = pickle_perfil['simp']
    else:
        par_sim = np.nan

    return df_datos, lat, lon, fecha, par_sim


def add_prof(filename):
    """
    Agrega una columna a df de profundidad (negativa), 'PROF', y lo guarda en la carpeta
    /prueba_paper/perfiles/filename.
    Necesita tener el archivo pickle con:
        fecha, lat, lon, df['PRES','SAL','TEMP','DENS']

    INPUTS
    filename: str.

    OUTPUTS
    df: dataframe con PRES, SAL, TEMP, DENS, PROF
    lat: float, latitud
    lon: float, longitud
    fecha: str, fecha en YYYY-MM-DD
    """
    import pickle
    import gsw

    df, lat, lon, fecha, par_sim = read_pickle_perfiles(filename)
    df['PROF'] = gsw.conversions.z_from_p(df['PRES'], lat)
    #Sobreescribo el archivo dentro de las carpetas 'perfiles'
    dic = {'nombre':filename[:3],
            'fecha':fecha,
            'lat':lat,
            'lon':lon,
            'df':df}
    pickle.dump(dic, open('../perfiles/'+filename, "wb" ) )

    return df, lat, lon, fecha


def add_simpson_parameter(filename):
    """
    Calcula el parametro de simpson del perfil, lo agrega al diccionario de la
    estacion en la carpeta 'perfiles'.
        dic = {'nombre':filename[:3],
            'fecha':fecha,
            'lat':lat,
            'lon':lon,
            'simp':par_sim,
            'df':df}

    Necesita tener el archivo pickle con:
        fecha, lat, lon, df['PRES','SAL','TEMP','DENS','PROF']


    INPUTS
    filename: str. Nombre del perfil.

    OUTPUTS
    par_sim: float.
        Parametro de Simpson

    """
    # PARAMETRO DE ESTABILIDAD DE SIMPSON #
    # S = (1/k) * integral[(rho-rho_medio)*g*z*dz]
    # Unidades
    # (1/k)*rho*g*z*deltaz
    # (1/m)*(kg/m^3)*(m/s^2)*m*m
    # kg/(m.s^2) = J.m^3

    import pickle
    import numpy as np
    # Perfil vertical de densidad inventado
    df, lat, lon, fecha, par_sim = read_pickle_perfiles(filename)

    # Densidad potencial
    rho = df['DENS'].values
    # Profundidad
    prof = df['PROF'].values

    # Delta de profundidad:
        # c/ medicion de dens es representativa de 'un poco' para arriba y 'un poco'
        # para abajo de su profundidad. 'un poco' es la mitad de la distancia
        # entre esa medicion y la que sigue
    deltaz = np.nan*np.ones_like(prof)
    deltaz[0] = np.abs(prof[0]) + np.abs((prof[0]- prof[1])/2)  # 1er valor: valido hasta la superficie
    for iz in range(1,len(prof)-1):
        deltaz[iz] = (np.abs(prof[iz-1]-prof[iz+1])/2)
    deltaz[-1] = np.abs(prof[-2]-prof[-1])/2                          # ultimo valor: valido solo 'un poco' para arriba

    # Gravedad
    g = 9.8
    # Densidad media del perfil
    rho_medio = np.nanmean(rho)
    # Profundidad de la columna de agua:
    k = prof[-1]
    # Creo la sumatoria
    sumatoria = 0
    for iz in range(0,len(prof)):
        sumatoria = sumatoria + (rho[iz]-rho_medio)*g*prof[iz]*deltaz[iz]

    # A la sumatoria la multiplico por 1/k
    par_sim = (1/k) * sumatoria

    # Sobreescribo el archivo dentro de la carpeta 'perfiles' con el parametro de simpson agregado.
    dic = {'nombre':filename[:3],
            'fecha':fecha,
            'lat':lat,
            'lon':lon,
            'simp':par_sim,
            'df':df}
    pickle.dump(dic, open('../perfiles/'+filename, "wb" ) )

    return df, lat, lon, fecha, par_sim
