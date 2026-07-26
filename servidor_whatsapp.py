import os
from flask import Flask, request
import pandas as pd

# Inicializamos la aplicación Flask
app = Flask(__name__)

# Nombre de tu archivo de Excel
archivo_excel = "Planificador.xlsx"

def buscar_en_excel(consulta):
    if not os.path.exists(archivo_excel):
        return "⚠️ No encuentro el archivo Planificador.xlsx en la carpeta."
    
    try:
        # Lee todas las pestañas del Excel
        excel_data = pd.read_excel(archivo_excel, sheet_name=None)
        consulta_lower = str(consulta).lower().strip()
        
        debug_filas = []
        # Recorre cada pestaña buscando coincidencias
        for hoja, df in excel_data.items():
            for index, row in df.iterrows():
                # Convertimos cada celda a string solo si no está vacía
                valores_fila = [str(val) for val in row.values if pd.notna(val)]
                fila_texto = " ".join(valores_fila).lower()
                debug_filas.append(fila_texto) # Guardamos para ver qué lee el bot
                
                if consulta_lower in fila_texto:
                    # Armamos el texto de forma segura filtrando nulos
                    detalle = " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)])
                    return f"📋 Encontrado en [{hoja}]:\n{detalle}"
        
        # Si no encuentra nada, te muestra un pedazo de lo que el bot leyó realmente en el Excel
        muestra = " // ".join(debug_filas[:2]) if debug_filas else "Excel vacío"
        return f"🔍 Busqué '{consulta_lower}', pero esto es lo que leí en el Excel: {muestra}"
            
    except Exception as e:
        return f"Error al leer el Excel: {str(e)}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # Obtiene el mensaje que mandaste desde WhatsApp
    mensaje_recibido = request.form.get('Body')
    
    # Busca la respuesta en tu Excel
    respuesta_excel = buscar_en_excel(mensaje_recibido)
    
    # Prepara la respuesta para WhatsApp en formato XML
    xml_respuesta = f"""<Response>
    <Message>{respuesta_excel}</Message>
</Response>"""
    
    return xml_respuesta, 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(port=5000)