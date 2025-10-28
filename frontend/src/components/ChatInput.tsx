/**
 * ChatInput Component
 * 
 * Message input textarea with send button
 */

import { useState, KeyboardEvent, useRef, useEffect } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSend: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSend,
  disabled = false,
  placeholder = 'Type your message...',
}) => {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px';
    }
  }, [message]);

  const handleSend = () => {
    if (message.trim() && !disabled) {
      onSend(message);
      setMessage('');
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="flex items-end space-x-2">
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={placeholder}
          disabled={disabled}
          rows={1}
          className="w-full px-4 py-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-100 disabled:text-gray-500 max-h-32 overflow-y-auto"
        />
        <div className="absolute bottom-2 right-2 text-xs text-gray-400">
          {disabled ? '' : 'Shift + Enter for new line'}
        </div>
      </div>
      <button
        onClick={handleSend}
        disabled={disabled || !message.trim()}
        className="btn btn-primary p-3 flex-shrink-0"
        title="Send message (Enter)"
      >
        <Send className="w-5 h-5" />
      </button>
    </div>
  );
};

export default ChatInput;
