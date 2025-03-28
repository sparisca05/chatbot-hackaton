import asyncio
import websockets

async def test_websocket():
    uri = "ws://127.0.0.1:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("Hola! Soy tu asistente virtual 🤖. ¿En qué puedo ayudarte?")

        while True:
            # Solicita el mensaje de prueba al usuario
            mensaje = input()

            # Envía el mensaje ingresado al WebSocket
            await websocket.send(mensaje)

            # Espera y recibe la respuesta del WebSocket
            print("Esperando respuesta del asistente...")
            response = await websocket.recv()
            print(f"{response}")

            # Termina la operación si el usuario ingresa 'salir'
            if mensaje.lower() == 'salir':
                print("Desconectando del WebSocket...")
                break

# Ejecuta la función de prueba
asyncio.get_event_loop().run_until_complete(test_websocket())