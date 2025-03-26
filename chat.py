import google.generativeai as genai
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import pandas as pd
import random

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

# Simulación de historial de conversación
historial = [
    {"role": "system", "content": "Eres un asistente que ayuda a negociar pagos con clientes."},
]

# Iniciar conversación por consola
print("💬 Chatbot de Negociación de Pagos (Escribe 'salir' para terminar)\n")

respuesta = 0

while True:
    user_input = input("Tú: ")
    if user_input.lower() == "salir":
        print("👋 Adiós!")
        break

    respuesta += 1

    # Agregar input del usuario al historial
    historial.append({"role": "user", "content": user_input})
    
    if (respuesta > 1):
        # Enviar historial completo a la IA
        response = model.generate_content([m["content"] for m in historial])
        
        # Agregar respuesta de la IA al historial
        historial.append({"role": "assistant", "content": response.text})
        print(f"🤖 Chatbot: {response.text}\n")
    else:
        # Generar valores aleatorios para crédito y días de mora
        credito = random.randint(100, 300)*10000
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
        print(f"🤖 Chatbot: {mensaje}\n")
