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
        
        resultados = []
        consulta_lower = str(consulta).lower()
        
        # Recorre cada pestaña buscando coincidencias
        for hoja, df in excel_data.items():
            for index, row in df.iterrows():
                fila_texto = " ".join(row.astype(str)).lower()
                if consulta_lower in fila_texto:
                    resultados.append(f"[{hoja}] " + " | ".join([f"{col}: {val}" for col, val in row.items() if pd.notna(val)]))
        
        if resultados:
            return "📋 Aquí tienes la información encontrada:\n\n" + "\n".join(resultados[:3])
        else:
            return "No encontré información relacionada con tu consulta en el Excel."
            
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
    # Corre Flask en el puerto 5000
    app.run(port=5000)