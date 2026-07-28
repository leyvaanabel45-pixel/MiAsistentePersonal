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
        # Lee TODAS las pestañas del Excel al mismo tiempo
        excel_data = pd.read_excel(archivo_excel, sheet_name=None)
        consulta_lower = str(consulta).lower().strip()
        
        resultados = []
        
        # Recorre cada pestaña (Universidad, Gastos, Deporte, Vida_social, etc.)
        for hoja, df in excel_data.items():
            # Recorre fila por fila dentro de esa pestaña
            for index, row in df.iterrows():
                # Revisa si la palabra que buscas está en alguna celda de esta fila
                fila_coincide = False
                for col, val in row.items():
                    if pd.notna(val) and consulta_lower in str(val).lower():
                        fila_coincide = True
                        break
                
                # Si encuentra coincidencia en esta fila, extrae los datos ordenados
                if fila_coincide:
                    detalles = []
                    for col, val in row.items():
                        if pd.notna(val):
                            detalles.append(f"*{col}*: {val}")
                    
                    item_resultado = f"📌 Encontrado en pestaña [{hoja}]:\n" + " | ".join(detalles)
                    if item_resultado not in resultados:
                        resultados.append(item_resultado)
        
        if resultados:
            # Te muestra hasta 3 coincidencias relevantes de cualquiera de las pestañas
            return "📋 Aquí tienes la información:\n\n" + "\n\n".join(resultados[:3])
        else:
            return f"No encontré registros sobre '{consulta}' en ninguna de tus pestañas del Excel."
            
    except Exception as e:
        return f"Error al leer el Excel: {str(e)}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_recibido = request.form.get('Body')
    respuesta_excel = buscar_en_excel(mensaje_recibido)
    
    xml_respuesta = f"""<Response>
    <Message>{respuesta_excel}</Message>
</Response>"""
    
    return xml_respuesta, 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(port=5000)