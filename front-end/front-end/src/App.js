import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI } from '@google/genai';

import Bot3D from './components/Bot3D/Bot3D';
import Chat from './components/Chat/Chat';
import './App.css';

const apiKey = process.env.REACT_APP_GOOGLE_GENAI_API_KEY;

if (!apiKey) {
  console.error("API Key is missing. Please set REACT_APP_GOOGLE_GENAI_API_KEY in your .env file.");
}

const ai = new GoogleGenAI({ apiKey });

const chat = ai.chats.create({
  model: "gemini-2.0-flash",
  config: {
    systemInstruction: "Te llamas Isabot y eres un asistente que debe realizar una negociación asertiva con un cliente que no puede pagar."
  },
  });

function App() {
  const historialChatBot = [ ]
  const [messages, setMessages] = useState([
    {
      text: "👋 Hola! Soy Isabot, tu Chatbot de Negociación de Pagos.\n Escribe algo para obtener tu estado de cuenta actual.",
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [isTyping, setIsTyping] = useState(false);
    
  const addBotMessage = (text) => {
    const newMessage = {
      text,
      sender: 'bot',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [newMessage, ...prev]);
  };

  const handleSendMessage = async (message) => {
    if (!message.trim()) return;

    // Añadir mensaje del usuario
    const userMessage = {
      text: message,
      sender: 'user',
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    setMessages(prev => [userMessage, ...prev]);
    setIsTyping(true);

    // Enviar mensaje al bot
    let accumulatedResponse = ""; // Variable to accumulate the response
    const response = await chat.sendMessageStream({
      message: message
    });

    for await (const chunk of response) {
      const text = chunk.text;
      if (text) {
        accumulatedResponse += text; // Accumulate the chunks
      }
    }

    setIsTyping(false);

    // Add the complete response as a single message
    if (accumulatedResponse) {
      addBotMessage(accumulatedResponse);
    }

    // Añadir respuesta del bot al historial
    historialChatBot.push(accumulatedResponse);
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