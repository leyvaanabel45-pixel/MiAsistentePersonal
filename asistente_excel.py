import os
import unicodedata
from flask import Flask, request
import pandas as pd

app = Flask(__name__)
archivo_excel = 'Planificador.xlsx'

def quitar_acentos(texto):
    nfkd_form = unicodedata.normalize('NFKD', str(texto))
    return "".join([c for c in nfkd_form if not unicodedata.combining(c)]).lower().strip()

def buscar_en_todo_el_excel(consulta):
    if not os.path.exists(archivo_excel):
        return "⚠️ No encuentro el archivo Planificador.xlsx."
    
    try:
        consulta_limpia = quitar_acentos(consulta)
        resultados = []
        
        # Leemos el archivo de Excel hoja por hoja de forma segura
        xls = pd.ExcelFile(archivo_excel)
        for hoja in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=hoja)
            
            # Si el nombre de la hoja coincide con lo que buscas
            if consulta_limpia in quitar_acentos(hoja):
                resumen = df.to_string(index=False)
                resultados.append(f"📂 Pestaña completa [{hoja}]:\n{resumen}")
                continue
            
            # Buscar en las filas y columnas
            for index, row in df.iterrows():
                fila_coincide = False
                for col, val in row.items():
                    if pd.notna(val) and consulta_limpia in quitar_acentos(val):
                        fila_coincide = True
                        break
                
                if fila_coincide:
                    detalles = []
                    for col, val in row.items():
                        if pd.notna(val):
                            detalles.append(f"*{col}*: {val}")
                    
                    item_resultado = f"📌 [{hoja}] -> " + " | ".join(detalles)
                    if item_resultado not in resultados:
                        resultados.append(item_resultado)
        
        if resultados:
            return "¡Hola Anabel! 📋 Encontré esto en tu Excel:\n\n" + "\n\n".join(resultados[:4])
        else:
            return f"No encontré ningún registro con '{consulta}' en tu Excel. ¡Prueba con otra palabra clave!"
            
    except Exception as e:
        return f"Error leyendo el Excel: {str(e)}"

@app.route("/whatsapp", methods=['POST'])
def whatsapp_reply():
    mensaje_recibido = request.form.get('Body', '')
    respuesta_excel = buscar_en_excel(mensaje_recibido)
    
    xml_respuesta = f"""<Response>
    <Message>{respuesta_excel}</Message>
</Response>"""
    
    return xml_respuesta, 200, {'Content-Type': 'text/xml'}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)