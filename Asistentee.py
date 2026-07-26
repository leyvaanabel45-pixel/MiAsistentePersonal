import pandas as pd

nombre_archivo = 'Planificador.xlsx'

df_proyectos = pd.read_excel(nombre_archivo, sheet_name='Proyectos')

print("--- ¡ÉXITO! TUS PROYECTOS DESDE EXCEL ---")
print(df_proyectos)
