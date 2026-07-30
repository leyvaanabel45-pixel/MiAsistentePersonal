Python

import os
import unicodedata
from flask import Flask, request
import pandas as pd

app = Flask(__name__)
archivo_excel = 'Planificador.xlsx'

def quitar_acentos(texto):
    # Limpia acentos, mayúsculas y espacios para que la búsqueda nunca falle por una tilde
    nfkd_form = unicodedata.normalize('NFKD', str(texto))
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()

def buscar_en_todo_el_excel(consulta):
    if not os.path.exists(archivo_excel):
        return "⚠️ No encuentro el archivo Planificador.xlsx."
    
    try:
        # Lee TODAS las pestañas del Excel al mismo tiempo
        excel_data = pd.read_excel(archivo_excel, sheet_name=None)
        consulta_limpia = quitar_acentos(consulta)
        
        resultados = []
        
        # Recorre cada pestaña del Excel
        for hoja, df in excel_data.items():
            # Si el nombre de la pestaña coincide con lo que buscas, te muestra la tabla completa de esa pestaña
            if consulta_limpia in quitar_acentos(hoja):
                resumen = df.to_string(index=False)
                resultados.append(f"📂 Pestaña completa [{hoja}]:\n{resumen}")
                continue
            
            # Si no es la pestaña, busca fila por fila en cada celda y columna
            for index, row in df.iterrows():
                fila_coincide = False
                for col, val in row.items():
                    if pd.notna(val) and consulta_limpia in quitar_acentos(val):
                        fila_coincide = True
                        break
                
                # Si encuentra algo en esta fila, arma el texto bonito con sus columnas
                if fila_coincide:
                    detalles = []
                    for col, val in row.items():
                        if pd.notna(val):
                            detalles.append(f"*{col}*: {val}")
                    
                    item_resultado = f"📌 [{hoja}] -> " + " | ".join(detalles)
                    if item_resultado not in resultados:
                        resultados.append(item_resultado)
        
        if resultados:
            # Devuelve hasta 5 resultados para que tengas toda la info necesaria
            return "¡Hola Anabel! 📋 Encontré esto en tu Excel:\n\n" + "\n\n".join(resultados[:5])
        else:
            return f"No encontré ningún registro con '{consulta}' en tu Excel. ¡Prueba con otra palabra clave!"
            
    except Exception as e:
        return f"Error al leer el Excel: {str(e)}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    # Obtiene el mensaje que escribes por WhatsApp
    mensaje_recibido = request.form.get('Body')
    
    # Busca por todo el Excel
    respuesta_excel = buscar_en_excel(mensaje_recibido)
    
    # Responde a Twilio/WhatsApp
    xml_respuesta = f"""<Response>
    <Message>{respuesta_excel}</Message>
</Response>"""
    
    return xml_respuesta, 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    app.run(port=5000)