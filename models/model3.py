import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_excel("../data/crudos/17-11-2023-09.xlsx", sheet_name=0)
#df = df[(df['Peso']>=5.05)&(df['Peso']<=5.65)]

df['Fecha'] = pd.to_datetime(df['Fecha'], format='%Y-%m-%d %H:%M:%S')
df['Peso'] = df['Peso'].round(2)

#print(df)

# Crear una columna que contenga los intervalos de 5 minutos
df['Intervalo'] = (df['Fecha'].dt.floor('3min'))

# Función para calcular la moda en un grupo
def calcular_moda(group):
    try:
        return group.mode().iloc[0]
    except IndexError:
        return None

# Agrupar por intervalos y calcular la desviación estándar y la moda de 'Peso'
result = df.groupby('Intervalo')['Peso'].agg(['std', calcular_moda, 'mean', 'median'])

# Renombrar las columnas para mayor claridad
result = result.rename(columns={'std': 'Desviación Estándar', 'calcular_moda': 'Moda', 'mean': 'PromedioC', 'median': 'Valor Medio'})

# Reiniciar el índice
result = result.reset_index()
result['Valor Medio'] = result['Valor Medio'].round(2)
result['PromedioC'] = result['PromedioC'].round(2)

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# A continuación, imprime el DataFrame para visualizarlo en su totalidad
print(result)

result.to_excel("../data/tratados3/17-11-2023-09.xlsx", index=False)

# Asegúrate de que la columna 'Intervalo' sea del tipo datetime
# result['Intervalo'] = pd.to_datetime(result['Intervalo'])

# Crear un gráfico con fondo negro y colores personalizados
# plt.figure(figsize=(12, 6), facecolor='black')
# plt.plot(result['Intervalo'], result['PromedioC'], color='skyblue')

# Configurar los colores de las marcas en los ejes
# plt.tick_params(axis='x', colors='white')
# plt.tick_params(axis='y', colors='white')

# plt.title('Gráfico de Promedio a lo largo del tiempo', color='white')

# Ajustar el color del fondo de los ejes
# ax = plt.gca()
# ax.set_facecolor('black')

# Mostrar la leyenda
# plt.legend()
# plt.grid(True, alpha=0.15)
# Mostrar el gráfico
# plt.show()