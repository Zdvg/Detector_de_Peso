# DEMORADO (PENDIENTE POR OPTIMIZAR)

import requests
import pandas as pd

df = pd.read_excel("../data/08-08-LL.xlsx")

# clave API de Google Maps
api_key = 'AIzaSyDEn81v6WC-8OZmV-3xoaUheV_osBFAo2Q'

# Iterar
altitudes = []
for idx, row in df.iterrows():
    lat = row['Latitud']
    lon = row['Longitud']
    url = f'https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lon}&key={api_key}'
    response = requests.get(url).json()
    if response['status'] == 'OK':
        altitude = response['results'][0]['elevation']
        altitudes.append(altitude)
        print("primer print", altitudes)
    else:
        altitudes.append(None)  # Manejar casos de error
        print("error", altitudes)

df['Altitud'] = altitudes
print(df)