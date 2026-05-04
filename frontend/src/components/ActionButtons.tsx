import React from 'react';
import { useChatStore } from '../store/useChatStore';
import { motion, AnimatePresence } from 'framer-motion';

export const ActionButtons: React.FC = () => {
  const { options, handleAction, loading } = useChatStore();

  if (!options || options.length === 0) return null;

  return (
    <div className="flex flex-wrap gap-2 mb-6 justify-center">
      <AnimatePresence>
        {options.map((option, index) => (
          <motion.button
            key={option + index}
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.9 }}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => !loading && handleAction(option)}
            disabled={loading}
            className="px-4 py-2 bg-blue-50 text-blue-700 rounded-full text-sm font-medium border border-blue-100 hover:bg-blue-100 transition-colors disabled:opacity-50"
          >
            {option}
          </motion.button>
        ))}
      </AnimatePresence>
    </div>
  );
};
