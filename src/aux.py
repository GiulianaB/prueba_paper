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

    pickle_perfil = pickle.load(open(filename, 'rb'))

    df_datos = pickle_perfil.get('data')
    lat = pickle_perfil.get('lat')
    lon = pickle_perfil.get('lon')
    fecha = pickle_perfil.get('fecha')

    return df_datos, lat, lon, fecha
