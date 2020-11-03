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

    if filename[:2] == 'bn': filename = 'Box_norte/' + filename
    if filename[:2] == 'bs': filename = 'Box_sur/' + filename
    pickle_perfil = pickle.load(open('../estaciones_CTD_tipo/' + filename, 'rb'))

    df_datos = pickle_perfil.get('data')
    lat = pickle_perfil.get('lat')
    lon = pickle_perfil.get('lon')
    fecha = pickle_perfil.get('fecha')

    return df_datos, lat, lon, fecha


def add_sigma_tita(filename):
    """
    Agrega una columna a df de dens-tita que se llama 'DENS',
    y lo guarda en la carpeta ../prueba_paper/perfiles/filename.
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
    df['DENS'] = gsw.density.sigma0(df['SAL'], df['TEMP']) + 1000
    # guardo en carpeta perfiles
    dic = {'nombre': filename[:3],
    'fecha': fecha,
    'lat': lat,
    'lon': lon,
    'df': df}
    pickle.dump(dic, open('../perfiles/' + filename, "wb"))

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
    Agrega una columna a df de profundidad (negativa) que se llama 'PROF',
    y lo guarda en la carpeta ../prueba_paper/perfiles/filename.
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
    # Sobreescribo el archivo dentro de las carpetas 'perfiles'
    dic = {'nombre': filename[:3],
            'fecha': fecha,
            'lat': lat,
            'lon': lon,
            'df': df}
    pickle.dump(dic, open('../perfiles/'+ filename, "wb"))

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
    df: dataframe con PRES, SAL, TEMP, DENS, PROF
    lat: float, latitud
    lon: float, longitud
    fecha: str, fecha en YYYY-MM-DD
    par_sim: float. Parametro de Simpson
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

    ind_ultimo = np.where(np.isnan(df['PRES']) == False)[0][-1]
    # Densidad potencial
    rho = df['DENS'].values[:ind_ultimo]
    # Profundidad
    prof = df['PROF'].values[:ind_ultimo]

    # Delta de profundidad:
        # c/ medicion de dens es representativa de 'un poco' para arriba y 'un poco'
        # para abajo de su profundidad. 'un poco' es la mitad de la distancia
        # entre esa medicion y la que sigue
    deltaz = np.nan*np.ones_like(prof)
    deltaz[0] = np.abs(prof[0]) + np.abs((prof[0]- prof[1])/2)  # 1er valor: valido hasta la superficie
    for iz in range(1,len(prof)-1):
        deltaz[iz] = (np.abs(prof[iz-1]-prof[iz+1])/2)
    deltaz[-1] = np.abs(prof[-2]-prof[-1])/2                    # ultimo valor: valido solo 'un poco' para arriba

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
    dic = {'nombre': filename[:3],
            'fecha': fecha,
            'lat': lat,
            'lon': lon,
            'simp': par_sim,
            'df': df}
    pickle.dump(dic, open('../perfiles/' + filename, "wb"))

    return df, lat, lon, fecha, par_sim

def pcm_umbral_densidad(z, rho, zref, umbral):
    """
    Calcula la profundidad de la capa de mezcla a partir
    de un perfil de rho en función de la profundidad.
    Se utiliza un criterio de umbral de densidad respecto
    a una profundidad de referencia.

    INPUTS
    z: array de profundidades.
    rho: array de densidad potencial
    zref: profundidad de referencia
    umbral: umbral de densidad.

    OUTPUTS
    zpcm: profundidad de la pcm
    """

    import numpy as np

    idx = (np.abs(z - zref)).argmin()
    z_nearest =  z[idx]                       # valor de profundidad mas cercano a zref

    for i, iz in enumerate(z):

        delta_theta = rho[i] - rho[idx]

        if delta_theta > umbral:
            break
    zpcm = iz

    return zpcm

def add_pcm_umbral_densidad(filename, zref, umbral):

    import pickle
    import numpy as np

    # Según la tesis de Valen, hay perfiles que son homogeneos, donde
    # los algoritmos llegan a resultados erroneos. Para el cálculo de la
    # PCM se excluyen los perfiles homogeneos ("si en un perfil la diferencia
    # entre la σθ de superficie y la σθ correspondiente a la máxima profundidad
    # medida es estrictamente menor que 0,15kg/m 3 entonces es considerado
    # homogéneo", Giunta 2016.)

    df, lat, lon, fecha, par_sim = read_pickle_perfiles(filename)

    ind_ultimo = np.where(np.isnan(df['PRES']) == False)[0][-1]
    # Densidad potencial
    rho = df['DENS'].values[:ind_ultimo]
    # Profundidad
    prof = df['PROF'].values[:ind_ultimo]

    rho_sup = rho[0]
    rho_fondo = rho[-1]

    if np.abs(rho_fondo-rho_sup) < 0.15:
        pcm = 0
    else:
        pcm = pcm_umbral_densidad(prof, rho, zref, umbral)


    dic = {'nombre': filename[:3],
            'fecha': fecha,
            'lat': lat,
            'lon': lon,
            'simp': par_sim,
            'pcm': pcm,
            'df': df}
    pickle.dump(dic, open('../perfiles/' + filename, "wb"))

    return df, lat, lon, fecha, par_sim, pcm


def profile_layout(df, lat, lon, fecha, par_sim, pcm):

    import numpy as np
    import gsw
    from bokeh.io import output_file, show, export_png
    from bokeh.layouts import row, column
    from bokeh.plotting import figure
    from bokeh.models import (Span, Div,
                              ColorBar,
                              FixedTicker,
                              LinearColorMapper,
                              PrintfTickFormatter)
    from bokeh.transform import linear_cmap

    tools = "hover, save, pan, box_zoom, reset, wheel_zoom"

    output_file("profile_features.html")

    y = df['PROF']
    x0 = df['TEMP']
    x1 = df['SAL']
    x2 = df['DENS']

    mint = x0.min()
    maxt = x0.max()
    mins = x1.min()
    maxs = x1.max()

    tempL = np.linspace(mint-1, maxt+1, 156)

    salL = np.linspace(mins-1, maxs+1, 156)

    Tg, Sg = np.meshgrid(tempL, salL)
    sigma_theta = gsw.sigma0(Sg, Tg)

    s1 = figure(plot_width=300, plot_height=500, background_fill_color="#fafafa",
                title="Temperature", toolbar_location="above", x_axis_location="above",
                tools=tools)
    s1.line(x0, y, color="#53777a", line_width=2)
    s1.circle(x0, y, size=4, color="#53777a", alpha=0.8, fill_color='white')
    hline = Span(location=pcm, dimension='width', line_color='black', line_width=1.5)
    s1.renderers.extend([hline])
    s1.xaxis.axis_label = "Temperature [°C]"
    s1.yaxis.axis_label = "Depth [m]"

    s2 = figure(plot_width=300, plot_height=500, background_fill_color="#fafafa",
                title="Salinity", toolbar_location="above", x_axis_location="above",
                tools=tools)
    hline = Span(location=pcm, dimension='width', line_color='black', line_width=1.5)
    s2.renderers.extend([hline])
    s2.line(x1, y, color="#c02942", line_width=2)
    s2.circle(x1, y, size=4, color="#c02942", alpha=0.8, fill_color='white')
    s2.xaxis.axis_label = "Salinity [PSU]"

    s3 = figure(plot_width=300, plot_height=500, background_fill_color="#fafafa",
                title="Density", toolbar_location="above", x_axis_location="above",
                tools=tools)
    hline = Span(location=pcm, dimension='width', line_color='black', line_width=1.5)
    s3.renderers.extend([hline])
    s3.line(x2, y, color="#d95b43", line_width=2)
    s3.circle(x2, y, size=4, color="#d95b43", alpha=0.8, fill_color='white')
    s3.xaxis.axis_label = "Density [kg m3]"

    s4 = figure(plot_width=300, plot_height=300, background_fill_color="#fafafa",
                title="TS diagram", toolbar_location="above",
                tools=tools, tooltips=[("x", "$x"), ("y", "$y"), ("value", "@image")])
    s4.x_range.range_padding = s4.y_range.range_padding = 0

    s4.circle(x1, x0, size=4, color="#f95b43", alpha=0.8, fill_color='white')
    s4.xaxis.axis_label = "Salinity [PSU]"
    s4.yaxis.axis_label = "Temperature [°C]"
    s4.image(image=[sigma_theta], x=mins, y=mint, dw=maxs-mins, dh=maxt-mint, palette="Spectral11", level="image")

    mapper = linear_cmap(field_name='y', palette='Spectral11', low=sigma_theta.min(), high=sigma_theta.max())

    levels = np.linspace(sigma_theta.min(), sigma_theta.max(), 11)
    color_bar = ColorBar(color_mapper=mapper['transform'],
                         major_label_text_font_size="8pt",
                         ticker=FixedTicker(ticks=levels),
                         formatter=PrintfTickFormatter(format='%.2f'),
                         label_standoff=6,
                         border_line_color=None,
                         location=(0, 0))

    s4.add_layout(color_bar, 'right')

    plots = row(s1, s2, s3, s4)
    final_plot = column(Div(text = f'<p>Lat: {lat:.2f}, Lon: {lon:.2f}, Fecha: {fecha} <p>PCM: {pcm:.2f}, Parámetro de Simpson: {par_sim:.2f}',
                        style={'font-size': '110%', 'color': 'black', 'font-weight': 'bold'}), plots)

    show(final_plot)

    export_png(final_plot, filename='../figs/' +'output-plot.png')
