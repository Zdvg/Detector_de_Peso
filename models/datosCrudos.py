import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("../data/08-08-LL.xlsx", sheet_name=0)
df['Fecha'] = pd.to_datetime(df['Fecha'])
df = df[(df['Peso']>=5.05)&(df['Peso']<=5.54)]

plt.figure(figsize=(10, 6))
plt.scatter(df['Fecha'], df['Peso'])
plt.xlabel('Fecha')  # Etiqueta del eje x
plt.ylabel('Voltios')  # Etiqueta del eje y
plt.title('Origin')

plt.show()