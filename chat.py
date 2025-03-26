import google.generativeai as genai
import os
from dotenv import load_dotenv

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

while True:
    user_input = input("Tú: ")
    if user_input.lower() == "salir":
        print("👋 Adiós!")
        break

    # Agregar input del usuario al historial
    historial.append({"role": "user", "content": user_input})

    # Enviar historial completo a la IA
    response = model.generate_content([m["content"] for m in historial])
    
    # Agregar respuesta de la IA al historial
    historial.append({"role": "assistant", "content": response.text})

    print(f"🤖 Chatbot: {response.text}\n")
