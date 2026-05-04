import React, { useState } from 'react';
import type { FormEvent } from 'react';
import { Send, Lock } from 'lucide-react';
import { useChatStore } from '../store/useChatStore';

export const InputBox: React.FC = () => {
  const [text, setText] = useState('');
  const { sendMessage, loading, ui } = useChatStore();

  const isLocked = ui?.lock_input;

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (text.trim() && !loading && !isLocked) {
      const msg = text;
      setText('');
      await sendMessage(msg);
    }
  };

  return (
    <form 
      onSubmit={handleSubmit}
      className="p-4 border-t border-gray-100 bg-white sticky bottom-0"
    >
      <div className="max-w-2xl mx-auto relative flex items-center">
        <input
          type="text"
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder={isLocked ? "Chatting with human agent..." : "Type your message..."}
          disabled={loading || isLocked}
          className={`w-full pl-6 pr-14 py-4 bg-gray-50 border-none rounded-full focus:ring-2 focus:ring-blue-500 transition-all outline-none text-gray-800 disabled:opacity-70 ${isLocked ? 'cursor-not-allowed bg-red-50' : ''}`}
        />
        <button
          type="submit"
          disabled={!text.trim() || loading || isLocked}
          className={`absolute right-2 p-2.5 rounded-full transition-all shadow-md active:scale-95 ${isLocked ? 'bg-gray-300' : 'bg-blue-600 text-white hover:bg-blue-700'}`}
        >
          {isLocked ? <Lock size={20} /> : <Send size={20} />}
        </button>
      </div>
    </form>
  );
};
