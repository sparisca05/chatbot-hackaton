import React from 'react';
import './Message.css';

const Message = ({ text, sender, timestamp, isTyping = false }) => {
  return (
    <div className={`message ${sender}-message ${isTyping ? 'typing' : ''}`}>
      <div className="message-content">
        {!isTyping && <div className="message-text">{text}</div>}
        {isTyping && (
          <div className="typing-indicator">
            <span></span>
            <span></span>
            <span></span>
          </div>
        )}
        <div className="message-time">{timestamp}</div>
      </div>
    </div>
  );
};

export default Message;