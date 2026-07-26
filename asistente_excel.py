import pandas as pd
import os

# Asegúrate de cambiar "tu_archivo.xlsx" por el nombre real de tu Excel
archivo_excel = "Planificador.xlsx"

def cargar_excel():
    if not os.path.exists(archivo_excel):
        print(f"⚠️ No encuentro el archivo '{archivo_excel}'. Guárdalo en esta misma carpeta.")
        return None
    
    # Lee todas las pestañas (categorías) del Excel
    excel_data = pd.read_excel(archivo_excel, sheet_name=None)
    return excel_data

def iniciar_chat():
    datos = cargar_excel()
    if datos is None:
        return

    print("\n✅ ¡Asistente de Excel listo y conectado!")
    print("📂 Pestañas/Categorías encontradas:", list(datos.keys()))
    print("Escribe 'salir' para terminar.\n")

    while True:
        pregunta = input("¿Qué quieres consultar de tu Excel?: ")
        if pregunta.lower() == 'salir':
            print("¡Hasta luego!")
            break

        encontrado = False
        for categoria, df in datos.items():
            texto_tabla = df.to_string(index=False).lower()
            if pregunta.lower() in texto_tabla or categoria.lower() in pregunta.lower():
                print(f"\n--- Encontrado en la categoría [{categoria}] ---")
                print(df)
                print("-" * 40)
                encontrado = True
        
        if not encontrado:
            print("\n❌ No encontré esa información exacta en tus pestañas. Prueba escribiendo el nombre de la categoría o un término clave.")

if __name__ == "__main__":
    iniciar_chat()