import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Header } from '../components/Header';
import { ChatWindow } from '../components/ChatWindow';
import { InputBox } from '../components/InputBox';
import { useChatStore } from '../store/useChatStore';

const ChatPage: React.FC = () => {
  const { businessId } = useParams<{ businessId: string }>();
  const { initSession, messages, setBusinessId, fetchBusinessInfo } = useChatStore();
  const initialized = React.useRef(false);

  useEffect(() => {
    if (businessId) {
      setBusinessId(businessId);
      fetchBusinessInfo(businessId);
    }
  }, [businessId]);

  useEffect(() => {
    if (!initialized.current && messages.length === 0) {
      initialized.current = true;
      initSession();
    }
  }, []);

  return (
    <div className="flex flex-col h-screen bg-white">
      <Header />
      <ChatWindow />
      <InputBox />
      
      <div className="max-w-2xl mx-auto w-full px-4 mb-2">
        <p className="text-[10px] text-center text-gray-400">
          Powered by AI Commerce Platform • Secure Checkout
        </p>
      </div>
    </div>
  );
};

export default ChatPage;
