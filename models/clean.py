import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("../data/08.xlsx", sheet_name=0)
df['Fecha'] = pd.to_datetime(df['Fecha'])

intervalo_tiempo = 5

df_procesado = pd.DataFrame()

for intervalo, grupo in df.groupby(pd.Grouper(key='Fecha', freq=f'{intervalo_tiempo}T')):
    # Calcula Q1, Q3 y el IQR para este grupo.
    Q1 = grupo['Peso'].quantile(0.25)
    Q3 = grupo['Peso'].quantile(0.75)
    IQR = Q3 - Q1

    # Definir límites para identificar outliers dentro de este grupo.
    lower_limit = Q1 - 1.5 * IQR
    upper_limit = Q3 + 1.5 * IQR

    # Identifica y reemplaza outliers por el valor promedio dentro de este grupo.
    outliers = (grupo['Peso'] < lower_limit) | (grupo['Peso'] > upper_limit)
    mean_value = grupo['Peso'].mean()
    grupo.loc[outliers, 'Peso'] = mean_value

    # Agrega el grupo procesado al DataFrame final.
    df_procesado = pd.concat([df_procesado, grupo])

df_procesado = df_procesado[(df_procesado['Peso']>=5.05)&(df_procesado['Peso']<=5.54)]
df_procesado = df_procesado[(df_procesado['Velocidad'] == 0)]
# print(df_procesado)

# plt.figure(figsize=(10, 6))
# plt.scatter(df_procesado['Fecha'], df_procesado['Peso'])
# plt.xlabel('Fecha')  # Etiqueta del eje x
# plt.ylabel('Voltios')  # Etiqueta del eje y
# plt.title('IQR')

# plt.show()

df_procesado.to_excel("../data/clean.xlsx", index=False)
