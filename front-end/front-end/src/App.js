import React, { useState, useEffect, useRef } from 'react';
import Bot3D from './components/Bot3D/Bot3D';
import Chat from './components/Chat/Chat';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [isTyping, setIsTyping] = useState(false);
  const ws = useRef(null);
  const [retryCount, setRetryCount] = useState(0);
  const maxRetries = 5;

  useEffect(() => {
    const connectWebSocket = () => {
      ws.current = new WebSocket('ws://127.0.0.1:8000/ws');

      ws.current.onopen = () => {
        console.log('Conexión establecida');
        setRetryCount(0);
        addBotMessage("¡Hola! Soy tu asistente virtual de SISTECREDITO. ¿En qué puedo ayudarte hoy?");
      };

      ws.current.onmessage = (event) => {
        setIsTyping(false);
        addBotMessage(event.data);
      };

      ws.current.onerror = (error) => {
        console.error('Error en WebSocket:', error);
        addBotMessage("Error de conexión. Por favor intenta nuevamente.");
        setIsTyping(false);
      };

      ws.current.onclose = () => {
        console.log('Conexión cerrada');
        if (retryCount < maxRetries) {
          setRetryCount(prev => prev + 1);
          setTimeout(connectWebSocket, 2000);
        } else {
          addBotMessage("No se pudo establecer la conexión. Por favor, inténtelo más tarde.");
        }
      };
    };

    connectWebSocket();

    return () => {
      if (ws.current) ws.current.close();
    };
  }, [retryCount]);

  const addBotMessage = (text) => {
    const newMessage = {
      text,
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [newMessage, ...prev]);
  };

  const handleSendMessage = (message) => {
    if (!message.trim() || !ws.current) return;

    // Añadir mensaje del usuario
    const userMessage = {
      text: message,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [userMessage, ...prev]);
    setIsTyping(true);

    // Enviar mensaje al backend
    if (ws.current.readyState === WebSocket.OPEN) {
      ws.current.send(message);
    } else {
      console.error('WebSocket no está conectado');
      setIsTyping(false);
      addBotMessage("No puedo conectarme al servidor. Recargue la página.");
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo">
            <div className="logo-icon">SC</div>
            <div className="logo-text">
              <h1>Asistente Virtual</h1>
              <p>SISTECREDITO - Negociación de Pagos</p>
            </div>
          </div>
          <div className="connection-status">
            <span className="status-dot"></span>
            <span>En línea</span>
          </div>
        </div>
      </header>

      {/* Contenido principal */}
      <main className="main-content">
        {/* Sección del Bot */}
        <section className="bot-section">
          <div className="bot-container">
            <Bot3D isTyping={isTyping} />
          </div>
        </section>
        
        {/* Sección del Chat */}
        <section className="chat-section">
          <Chat 
            messages={messages} 
            onSendMessage={handleSendMessage} 
            isTyping={isTyping}
          />
        </section>
      </main>
    </div>
  );
}

export default App;