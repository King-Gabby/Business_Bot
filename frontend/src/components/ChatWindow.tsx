import React, { useEffect, useRef } from 'react';
import { useChatStore } from '../store/useChatStore';
import { MessageBubble } from './MessageBubble';
import { ActionButtons } from './ActionButtons';
import { motion } from 'framer-motion';

export const ChatWindow: React.FC = () => {
  const { messages, loading, card } = useChatStore();
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, loading]);

  return (
    <main 
      ref={scrollRef}
      className="flex-1 overflow-y-auto p-4 bg-gray-50/50 scroll-smooth"
    >
      <div className="max-w-2xl mx-auto py-4">
        {/* Chat history starts empty as per Phase 4 instructions */}
        
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}

        {loading && (
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex justify-start mb-4"
          >
            <div className="bg-white p-4 rounded-2xl rounded-tl-none border border-gray-100 flex gap-1">
              <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0s' }} />
              <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
              <span className="w-1.5 h-1.5 bg-gray-300 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
            </div>
          </motion.div>
        )}

        {/* Dynamic Card Display */}
        {card && (
          <div className="mb-6">
            {card.type === 'product_grid' ? (
              <div className="grid grid-cols-2 gap-3">
                {card.items?.map((item: any, idx: number) => (
                  <div key={idx} className="bg-white p-4 rounded-2xl border border-gray-100 shadow-sm">
                    <p className="font-bold text-gray-800 text-sm">{item.name}</p>
                    <p className="text-blue-600 font-bold text-sm mt-1">{item.price}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="bg-white p-5 rounded-2xl border-l-4 border-blue-600 shadow-sm">
                <h3 className="font-bold text-gray-800 text-lg">{card.name}</h3>
                <p className="text-blue-600 font-bold text-xl mt-1">{card.price}</p>
                <p className="text-xs text-gray-500 mt-2">Available for immediate delivery.</p>
              </div>
            )}
          </div>
        )}

        <ActionButtons />
      </div>
    </main>
  );
};
