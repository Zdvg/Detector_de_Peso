import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

df = pd.read_excel("../data/crudos/18-10-2023.xlsx", sheet_name=0)
columnas = ['Fecha','Velocidad', 'Grados', 'Voltaje', 'Peso']
df = df[columnas]
#df = df[df['Velocidad']==0]

max_value = df['Peso'].max()
min_value = df['Peso'].min()

print('Máximo: ', max_value, 'Mínimo: ', min_value) 

df['Fecha']=pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')

intervalo_tiempo = 2

df['Fecha'] = df['Fecha'] - pd.to_timedelta(df['Fecha'].dt.minute % intervalo_tiempo, unit='m')

df['Intervalo'] = df['Fecha'].dt.strftime('%H:%M')

resultados = pd.DataFrame(columns=['Intervalo', 'Moda', 'Media', 'Mediana', 'Máximo', 'Mínimo', 'Varianza'])

for intervalo, grupo in df.groupby('Intervalo'):
    moda = grupo['Peso'].mode().values[0]
    media = grupo['Peso'].mean()
    mediana = grupo['Peso'].median()
    maximo = grupo['Peso'].max()
    minimo = grupo['Peso'].min()
    varianza = grupo['Peso'].var()
    
    resultados = pd.concat([resultados, pd.DataFrame({'Intervalo': [intervalo], 'Moda': [moda], 'Media': [media], 'Mediana': [mediana], 'Máximo': [maximo], 'Mínimo': [minimo], 'Varianza': [varianza]})], ignore_index=True)

resultados_filtrados = resultados[resultados['Varianza'] <= 0.0009]
mediaDF = resultados_filtrados[['Intervalo', 'Media']]
print(mediaDF)


# SEGUNDO CÁLCULO DE LA MEDIA


mediaDF['Intervalo'] = pd.to_datetime(mediaDF['Intervalo'])

intervalo_tiempo = '10T'
mediaDF['Intervalo'] = mediaDF['Intervalo'] - pd.to_timedelta(mediaDF['Intervalo'].dt.minute % 10, unit='m')

# Agrupar los datos en intervalos de 10 minutos y calcular la media
mediaDF = mediaDF.groupby('Intervalo').mean()

mediaDF = mediaDF.reset_index()
print(mediaDF)

mediaDF.to_excel("../data/nuevo_gps/18-10/p-18-10.xlsx", index=False)

plt.figure(figsize=(12, 6))
plt.plot(mediaDF['Intervalo'], mediaDF['Media'], label='Media')
plt.xlabel('Hora')
plt.ylabel('Voltaje')
plt.title('COMPORTAMIENTO DEL SENSOR PARA EL 18 DE OCTUBRE')
plt.legend()
plt.grid(True)
plt.show()