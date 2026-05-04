import React from 'react';
import { useChatStore } from '../store/useChatStore';
import { Store, Bot, RotateCcw } from 'lucide-react';

export const Header: React.FC = () => {
  const { resetChat, initSession, businessName } = useChatStore();

  const handleReset = () => {
    resetChat();
    initSession();
  };

  return (
    <header className="bg-white border-b border-gray-100 p-4 sticky top-0 z-10 shadow-sm">
      <div className="flex items-center justify-between max-w-2xl mx-auto">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-50 rounded-full flex items-center justify-center">
            <Store className="text-blue-600" size={20} />
          </div>
          <div>
            <h1 className="font-bold text-gray-800 text-lg leading-tight truncate max-w-[180px]">
              {businessName}
            </h1>
            <p className="text-xs text-gray-500">Premium Fashion Assistant</p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <button 
            onClick={handleReset}
            className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-full transition-colors"
            title="Reset Chat"
          >
            <RotateCcw size={18} />
          </button>

          <span className="flex items-center gap-1.5 px-3 py-1 bg-green-50 text-green-700 rounded-full text-xs font-semibold">
            <Bot size={14} /> AI Online
          </span>
        </div>
      </div>
    </header>
  );
};
