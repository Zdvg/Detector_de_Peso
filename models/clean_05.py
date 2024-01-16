import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("../data/nuevo_gps/25-10/21-10.xlsx", sheet_name=0)
#df = df[(df['Peso']>=5.05)&(df['Peso']<=5.65)]

df['Fecha']=pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')

intervalo_tiempo = 10

#df['Fecha'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.minute % intervalo_tiempo, unit='m')

df['Intervalo'] = df['Fecha'].dt.strftime('%H:%M')

valores_frecuentes_por_intervalo = []

for intervalo, grupo in df.groupby('Intervalo'):
    conteo_valores = grupo['Peso'].value_counts()

    # Encuentra el valor más frecuente y su frecuencia
    moda = conteo_valores.idxmax()
    frecuencia = conteo_valores.max()

    # Filtra los valores que cumplen con la condición
    valores_filtrados = conteo_valores[conteo_valores > 0.50 * frecuencia].index.tolist()

    valores_frecuentes_por_intervalo.append({'Intervalo': intervalo, 'Valores': valores_filtrados})

# Crea un DataFrame con los resultados
df_resultado = pd.DataFrame(valores_frecuentes_por_intervalo)

# Establece la opción de pandas para mostrar todas las filas y columnas sin truncamiento
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

print(df_resultado)

max_values = []

# Iterar a través de las filas del DataFrame df_resultado
for index, row in df_resultado.iterrows():
    # Obtener la lista de valores para el intervalo actual
    values = row['Valores']

    # Si la lista no está vacía, calcular el valor máximo y agregarlo a max_values
    if values:
        values = [float(str(value).replace(',', '.')) for value in values]
        max_values.append(max(values))

# Agregar la columna 'Max_Value' al DataFrame df_resultado
df_resultado['Max_Value'] = max_values

print("="*80)
print(df_resultado)


# #CONVERSIÓN

# mapeo_toneladas = {
#     5.05: 0, 5.06: 0.4, 5.07: 0.7, 5.08: 1, 5.09: 1.4, 5.10: 1.7,
#     5.11: 2, 5.12: 2.4, 5.13: 2.7, 5.14: 3, 5.15: 3.4, 5.16: 3.7,
#     5.17: 4, 5.18: 4.4, 5.19: 4.7, 5.20: 5, 5.21: 5.4, 5.22: 5.7,
#     5.23: 6, 5.24: 6.4, 5.25: 6.7, 5.26: 7, 5.27: 7.4, 5.28: 7.7,
#     5.29: 8, 5.3: 8.4, 5.31: 8.7, 5.32: 9, 5.33: 9.4, 5.34: 9.7,
#     5.35: 10, 5.36: 10.4, 5.37: 10.7, 5.38: 11, 5.39: 11.4, 5.4: 11.7,
#     5.41: 12, 5.42: 12.4, 5.43: 12.7, 5.44: 13, 5.45: 13.4, 5.46: 13.7,
#     5.47: 14, 5.48: 14.4, 5.49: 14.7, 5.5: 15, 5.51: 15.4, 5.52: 15.7,
#     5.53: 16, 5.54: 16.4, 5.55: 16.7, 5.56: 17, 5.57: 17.4, 5.58: 17.7,
#     5.59: 18, 5.6: 18.4, 5.61: 18.7, 5.62: 19
# }

# df_resultado['Toneladas'] = df_resultado['Max_Value'].map(mapeo_toneladas)

# print("="*80)
# print(df_resultado)

df_resultado.to_excel("../data/nuevo_gps/21-10/21-10-10.xlsx", index=False)


