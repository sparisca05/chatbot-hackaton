from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import random
import pdf
import logging

app = FastAPI()

# Permitir CORS para frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ruta principal que sirve el frontend
@app.get("/", response_class=HTMLResponse)
async def get():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)

logging.basicConfig(level=logging.INFO)
logging.info("Starting server")

# WebSocket para comunicación en tiempo real
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    logging.info("WebSocket connection attempt")
    await websocket.accept()
    historial = [
        {"role": "system", "content": "Eres un asistente que debe realizar una negociación asertiva con un cliente que no puede pagar. Además, debes tener de base estas respuestas predefinidas: " + pdf.pdf()},
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
            logging.info(f"Received message: {data}")
            respuesta += 1

            # Agregar input del usuario al historial
            historial.append({"role": "user", "content": data})
            
            if respuesta == 1:
                # Generar valores aleatorios para crédito y días de mora
                credito = str(random.randint(100, 300) * 10000)
                dias = str(random.randint(10, 90))
                
                historial.append({"role": "context", "content": "proporciona al usuario una respuesta basada en estos ejemplos (separados por ;) y teniendo en cuenta que el crédito es " + credito + " y los dias en mora " + dias + ": " + pdf.train()} )
                response = model.generate_content([m["content"] for m in historial])
                historial.append({"role": "assistant", "content": response.text})
                await websocket.send_text(response.text)

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
            logging.info("WebSocket disconnected, attempting to reconnect...")
            break
        except Exception as e:
            logging.error(f"WebSocket error: {e}")
            await websocket.close()
            break

# Cargar archivos Excel
historial_df = pd.read_csv("./Files/HistoricoContactCenter.csv")
conversaciones_df = pd.read_excel("./Files/negociaciones_compromiso_pago.xlsx")

# Contar cuántas veces se ha ofrecido cada alternativa
alternativas_exitosas = historial_df["Respuesta"].value_counts().head(20)

# Cargar variables de entorno
load_dotenv()
GEMINI_API_KEY = os.getenv("API_KEY")

# Configurar Google Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")
