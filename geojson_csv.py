import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon

# Cargar el archivo CSV
puntos = pd.read_csv(r'C:\Users\USUARIO6\Documents\Julio\POWER BI\lat_long_dom.csv')

# Limpiar los datos de latitud y longitud
puntos['latitud'] = pd.to_numeric(puntos['latitud'].str.replace(r'[^\d.-]', '', regex=True), errors='coerce')
puntos['longitud'] = pd.to_numeric(puntos['longitud'].str.replace(r'[^\d.-]', '', regex=True), errors='coerce')

# Eliminar filas con valores no numéricos (NaN) en latitud o longitud
puntos = puntos.dropna(subset=['latitud', 'longitud'])

# Convertir los puntos a un GeoDataFrame
puntos_gdf = gpd.GeoDataFrame(
    puntos, 
    geometry=gpd.points_from_xy(puntos.longitud, puntos.latitud),
    crs="EPSG:4326"
)

# Crear un polígono a partir de las coordenadas de la geocerca
coordenadas_geocerca = [(-108.9945,25.7902172), (-109.0215369,25.7505768), (-108.9890139,25.7319358), (-108.9631799,25.7725598), (-108.9945,25.7902172)]
poligono_geocerca = Polygon(coordenadas_geocerca)
geocerca_gdf = gpd.GeoDataFrame(index=[0], geometry=[poligono_geocerca], crs="EPSG:4326")

# Realizar la unión espacial para obtener solo los puntos dentro de la geocerca
puntos_dentro_geocerca = gpd.sjoin(puntos_gdf, geocerca_gdf, predicate='within')

# Exportar el resultado a un archivo CSV en el escritorio
puntos_dentro_geocerca.drop(columns='geometry').to_csv(r'C:\Users\USUARIO6\Desktop\puntos_dentro_geocerca.csv', index=False)

print("Proceso completado. El archivo se ha exportado en el escritorio.")


