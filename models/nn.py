import pandas as pd
import numpy as np

df = pd.read_excel("../data/nuevo_gps/19-10/19-10-2023.xlsx", sheet_name=0)
df['Peso'] = df['Peso'].round(2)
df = df[df['Peso']>=2.00]


df['Fecha']=pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')

intervalo_tiempo = 10

df['Fecha'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.minute % intervalo_tiempo, unit='m')

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

max_values = []
promedio = []

# Iterar a través de las filas del DataFrame df_resultado
for index, row in df_resultado.iterrows():
    # Obtener la lista de valores para el intervalo actual
    values = row['Valores']

    # Si la lista no está vacía, calcular el valor máximo y agregarlo a max_values
    if values:
        values = [float(str(value).replace(',', '.')) for value in values]
        max_values.append(max(values))
        promedio.append(np.mean(values))

# Agregar la columna 'Max_Value' al DataFrame df_resultado
df_resultado['Max_Value'] = max_values
df_resultado['Promedio'] = promedio
df_resultado['Promedio'] = df_resultado['Promedio'].round(2)

print("="*80)
print(df_resultado)

#df_resultado.to_excel("../data/nuevo_gps/21-10/21-10-10.xlsx", index=False)