import React from 'react';
import type { Message } from '../types/chat';
import { motion } from 'framer-motion';

interface Props {
  message: Message;
}

export const MessageBubble: React.FC<Props> = ({ message }) => {
  const isBot = message.sender === 'bot';

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className={`flex ${isBot ? 'justify-start' : 'justify-end'} mb-4`}
    >
      <div
        className={`max-w-[85%] p-4 rounded-2xl shadow-sm text-sm leading-relaxed ${
          isBot
            ? 'bg-white text-gray-800 rounded-tl-none border border-gray-100'
            : 'bg-blue-600 text-white rounded-tr-none'
        }`}
      >
        <p className="whitespace-pre-wrap">{message.text}</p>
        <p className={`text-[10px] mt-1.5 opacity-60 text-right`}>
          {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>
    </motion.div>
  );
};
