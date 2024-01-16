import pandas as pd
import numpy as np 

df = pd.read_excel("../data/proof_80%/21-07.xlsx", sheet_name=0)
columnas = ['Intervalo','Toneladas']
df_p1 = df[columnas]

#Inicializacion de la variable
estado = 'sin_encontrar'
anterior = None
fila_en_validacion = None
segunda_fila_de_validacion = None

#Dato final que saldrá en el panel
filas_seleccionadas = []

for indice, fila in df_p1.iterrows():
    if estado == "sin_encontrar":
        if (fila['Toneladas'] == 0 or fila['Toneladas'] == 0.4 or fila['Toneladas'] == 0.7):
            filas_seleccionadas.append(fila)
            anterior = fila
            estado = "encontrado"


    elif estado == "encontrado":
        diferencia = fila['Toneladas'] - anterior['Toneladas'] #¿se actualizó? -- SI

        if 0 <= diferencia <= 1.0:
            filas_seleccionadas.append(fila)
            anterior = fila #Se actualiza
            estado = 'encontrado'

        elif diferencia < 0 and fila['Toneladas'] <= anterior['Toneladas']: 
            estado = 'encontrado'
            # El anterior es el mismo

        elif diferencia < 0 and anterior['Toneladas'] <= fila['Toneladas']:
            filas_seleccionadas.append(fila)
            anterior = fila
            estado = 'encontrado' #Revisar la lógica

        else:
            estado = "validacion"  # Se supone 1 < diferencia
            fila_en_validacion = fila


    elif estado == "validacion": 
        diferencia = fila['Toneladas'] - fila_en_validacion['Toneladas']

        if 0 <= diferencia < 1.0:
            filas_seleccionadas.append(fila_en_validacion) 
            estado = 'encontrado'
            anterior = fila_en_validacion

        elif fila['Toneladas'] == fila_en_validacion['Toneladas']:
            filas_seleccionadas.append(fila) 
            estado = 'encontrado'
            anterior = fila_en_validacion 

        elif diferencia < -1 and fila['Toneladas'] < anterior['Toneladas']:
            estado = 'segunda_validacion'

        elif diferencia < -1 and anterior['Toneladas'] < fila['Toneladas']:
            fila_en_validacion = fila #Se actualiza la fila de validación
            estado = 'validacion' 
        
        elif -1 <= diferencia < 0 and fila['Toneladas'] < anterior['Toneladas']:
            estado = 'segunda_validacion'
        
        elif -1 <= diferencia < 0 and anterior['Toneladas'] < fila['Toneladas']:
            fila_en_validacion = fila
            estado = 'validacion'


        else: #Caso en que aumente
            estado = 'segunda_validacion_por_aumento'
            segunda_fila_de_validacion = fila


    elif estado == "segunda_validacion_por_aumento":
        
        
        if anterior['Toneladas'] < fila['Toneladas']:
            minimo = min(fila['Toneladas'], fila_en_validacion['Toneladas'], segunda_fila_de_validacion['Toneladas'])
            
            if fila['Toneladas'] == minimo and fila['Toneladas'] >= anterior['Toneladas']:
                filas_seleccionadas.append(fila)
                estado = 'encontrado'
                anterior = fila 
            
            elif fila_en_validacion['Toneladas'] == minimo and fila['Toneladas'] >= anterior['Toneladas']:
                filas_seleccionadas.append(fila_en_validacion)
                estado = 'encontrado'
                anterior = fila_en_validacion
            
            elif segunda_fila_de_validacion['Toneladas']== minimo and fila['Toneladas'] >= anterior['Toneladas']:
                filas_seleccionadas.append(segunda_fila_de_validacion)
                estado = 'encontrado'
                anterior = segunda_fila_de_validacion

        
        elif fila['Toneladas'] < anterior['Toneladas']:
            estado = 'validacion' #Poner el limite de los 30 minutos 



    elif estado == "segunda_validacion":
        
        
        if anterior['Toneladas'] < fila['Toneladas']:
            minimo = min(fila['Toneladas'], fila_en_validacion['Toneladas'])
            
            if fila['Toneladas'] == minimo and fila['Toneladas'] >= anterior['Toneladas']:
                filas_seleccionadas.append(fila)
                estado = 'encontrado'
                anterior = fila 
            
            elif fila_en_validacion['Toneladas'] == minimo and fila['Toneladas'] >= anterior['Toneladas']:
                filas_seleccionadas.append(fila_en_validacion)
                estado = 'encontrado'
                anterior = fila_en_validacion
        
        elif fila['Toneladas'] < anterior['Toneladas']:
            estado = 'validacion' #Poner el limite de los 30 minutos      

# Crear un nuevo DataFrame con las filas seleccionadas
df_panel = pd.DataFrame(filas_seleccionadas, columns=df_p1.columns)

# Imprimir el nuevo DataFrame
print("DataFrame con las filas seleccionadas:")
print(df_panel)
print('Longitud para el panel: ', len(df_panel), 'Longitud del algoritmo: ', len(df_p1))