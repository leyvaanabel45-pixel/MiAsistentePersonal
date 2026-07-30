import pandas as pd
from twilio.rest import Client

# Credenciales de tu cuenta de Twilio
account_sid = 'AC600684fc5abb0716ed2f7bdf8f169311'
auth_token = '200353175915a3db6a4eec6cda1414d3'  # Reemplaza esto con tu token secreto de Twilio

client = Client(account_sid, auth_token)

# Número de Twilio (el que viene por defecto para pruebas)
twilio_whatsapp_number = 'whatsapp:+14155238886'
# Tu número personal de WhatsApp al que enviaste el mensaje de unión
tu_numero_whatsapp = 'whatsapp:+559584044094'

archivo = 'Planificador.xlsx'

def consultar_datos_y_enviar(palabra_clave):
    df = pd.read_excel(archivo, sheet_name='Proyectos')
    resultado = df[df.astype(str).apply(lambda x: x.str.contains(palabra_clave, case=False)).any(axis=1)]
    
    if not resultado.empty:
        mensaje_texto = f"¡Hola Anabel! 📋 Encontré esto en tu Excel:\n\n{resultado.to_string(index=False)}"
    else:
        mensaje_texto = "No encontré ningún registro con esa palabra en tu Excel."
        
    # Enviar el mensaje a través de WhatsApp con Twilio
    message = client.messages.create(
        body=mensaje_texto,
        from_=twilio_whatsapp_number,
        to=tu_numero_whatsapp 
    )
    print(f"¡Mensaje enviado a tu WhatsApp con éxito! SID: {message.sid}")

# Ejecutamos la función buscando "Licencia"
consultar_datos_y_enviar("Licencia")