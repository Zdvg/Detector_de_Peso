import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("../data/clean.xlsx")

# Asegúrate de que la columna 'Fecha' esté en formato datetime
df['Fecha'] = pd.to_datetime(df['Fecha'])

# Define el intervalo de tiempo 
intervalo_tiempo = 15

# Agrupa los datos en intervalos de 30 minutos y calcula la media
df_agrupado = df.groupby(pd.Grouper(key='Fecha', freq=f'{intervalo_tiempo}T')).mean()

# # Crear la gráfica de líneas
# plt.figure(figsize=(12, 6))
# plt.plot(df_agrupado.index, df_agrupado['Peso'], label='Peso', marker='o')
# plt.plot(df_agrupado.index, df_agrupado['Altitud'], label='Altitud', marker='o')
# plt.xlabel('Fecha')
# plt.ylabel('Media')
# plt.title('Medias en intervalos de 30 minutos')
# plt.legend()
# plt.grid(True)

# # Mostrar la gráfica
# plt.show()

# Crear una figura con dos subplots, una encima de la otra
plt.figure(figsize=(12, 8))  # Ancho x Alto de la figura

# Primer subplot para el Peso
plt.subplot(2, 1, 1)  # 2 filas, 1 columna, primer subplot
plt.plot(df_agrupado.index, df_agrupado['Peso'], label='Peso', marker='o')
plt.xlabel('Fecha')
plt.ylabel('Peso')
plt.title('Medias en intervalos de 15 minutos - Peso')
plt.legend()
plt.grid(True)

# Segundo subplot para la Altitud
plt.subplot(2, 1, 2)  # 2 filas, 1 columna, segundo subplot
plt.plot(df_agrupado.index, df_agrupado['Altitud'], label='Altitud', marker='o')
plt.xlabel('Fecha')
plt.ylabel('Altitud')
plt.title('Medias en intervalos de 15 minutos - Altitud')
plt.legend()
plt.grid(True)

# Ajustar el espacio entre los subplots para evitar solapamientos
plt.tight_layout()

# Mostrar la figura con ambos subplots
plt.show()