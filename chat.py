from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import random

app = FastAPI()

# Montar directorio estático para archivos frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Ruta principal que sirve el frontend
@app.get("/", response_class=HTMLResponse)
async def get():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

# WebSocket para comunicación en tiempo real
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    historial = [
        {"role": "system", "content": "Eres un asistente que ayuda a negociar pagos con clientes. Y debes tener de base estas respuestas predefinidas: "},
    ]
    respuesta = 0

    def inferContext(mensaje):
        historial.append({"role": "system", "content": "Define a cuál de las siguientes opciones: 1.Ampliar cuotas 2.Reducir montos 3.Disminuir intereses 4.Otra. Se refiere este mensaje: " + mensaje + " y dame una respuesta con una solución propuesta."})
        response = model.generate_content([m["content"] for m in historial])
        historial.append({"role": "assistant", "content": response.text})
        return response

    while True:
        try:
            data = await websocket.receive_text()
            respuesta += 1

            # Agregar input del usuario al historial
            historial.append({"role": "user", "content": data})
            
            if respuesta == 1:
                # Generar valores aleatorios para crédito y días de mora
                credito = random.randint(100, 300) * 10000
                dias = random.randint(10, 90)
                
                # Calcular cuotas quincenales y mensuales
                cuotas_quincenales = round(credito / 6, 2)  # 6 biweekly payments in 3 months
                cuotas_mensuales = round(credito / 3, 2)    # 3 monthly payments in 3 months
                
                # Formatear el mensaje
                mensaje = (f"Tienes un crédito de ${credito:,} y {dias} días de mora. "
                        f"Podemos dividirlo en 6 cuotas quincenales de ${cuotas_quincenales:,} "
                        f"o en 3 cuotas mensuales de ${cuotas_mensuales:,}. "
                        "¿Cuál opción te parece que se adapta mejor a tus necesidades?")
                historial.append({"role": "assistant", "content": mensaje})
                await websocket.send_text(mensaje)
            elif respuesta == 2:
                # Inferir contexto
                response = inferContext(data)
                historial.append({"role": "system", "content": "Responde al cliente basado en esta respuesta: " + response.text})
            else: 
                # Enviar historial completo a la IA
                response = model.generate_content([m["content"] for m in historial])
                
                # Agregar respuesta de la IA al historial
                historial.append({"role": "assistant", "content": response.text})
                await websocket.send_text(response.text)
        except WebSocketDisconnect:
            break

# Cargar archivos Excel
historial_df = pd.read_csv("./Files/HistoricoContactCenter.csv")
conversaciones_df = pd.read_excel("./Files/negociaciones_compromiso_pago.xlsx")

# Contar cuántas veces se ha ofrecido cada alternativa
alternativas_exitosas = historial_df["Respuesta"].value_counts().head(20)
print(alternativas_exitosas)

# Cargar variables de entorno
load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")

# Configurar Google Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
