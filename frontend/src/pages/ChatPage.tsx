/**
 * Chat Page (Alternative with Custom Hook)
 * 
 * Complete RAG chat interface using the useChat hook
 * This is an optional alternative to the main ChatPage.tsx
 */

import { useEffect, useRef, useState } from 'react';
import { MessageSquare, Trash2, Download, AlertCircle } from 'lucide-react';
import { useChat } from '@/hooks';
import ChatInput from '@/components/ChatInput';
import ChatMessages from '@/components/ChatMessages';
import ChatSettings from '@/components/ChatSettings';
import { downloadTextFile } from '@/utils';

interface ChatSettingsState {
  topK: number;
  searchType: 'semantic' | 'keyword' | 'hybrid' | 'context';
  temperature: number;
  maxTokens: number;
  includeMetadata: boolean;
}

const ChatPageWithHook: React.FC = () => {
  const {
    messages,
    sources,
    isSending,
    error,
    sendMessage,
    clearChat,
    clearError,
    exportChat,
  } = useChat();

  const [showSettings, setShowSettings] = useState(false);
  const [settings, setSettings] = useState<ChatSettingsState>({
    topK: 5,
    searchType: 'semantic',
    temperature: 0.7,
    maxTokens: 500,
    includeMetadata: true,
  });

  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    await sendMessage(content, {
      top_k: settings.topK,
      search_type: settings.searchType,
      temperature: settings.temperature,
      max_tokens: settings.maxTokens,
      include_metadata: settings.includeMetadata,
    });
  };

  const handleClearChat = () => {
    if (messages.length === 0) return;

    if (confirm('Are you sure you want to clear the chat history?')) {
      clearChat();
    }
  };

  const handleExportChat = () => {
    if (messages.length === 0) {
      alert('No messages to export');
      return;
    }

    const exportText = exportChat();
    downloadTextFile(exportText, `chat-export-${new Date().getTime()}.txt`);
  };

  const handleSettingsChange = (newSettings: Partial<ChatSettingsState>) => {
    setSettings({ ...settings, ...newSettings });
  };

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)]">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">RAG Chat</h1>
          <p className="mt-1 text-sm text-gray-600">
            Chat with your documents using AI
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={() => setShowSettings(!showSettings)}
            className="btn btn-secondary text-sm"
          >
            {showSettings ? 'Hide' : 'Show'} Settings
          </button>
          <button
            onClick={handleExportChat}
            disabled={messages.length === 0}
            className="btn btn-secondary inline-flex items-center text-sm"
          >
            <Download className="w-4 h-4 mr-2" />
            Export
          </button>
          <button
            onClick={handleClearChat}
            disabled={messages.length === 0}
            className="btn btn-danger inline-flex items-center text-sm"
          >
            <Trash2 className="w-4 h-4 mr-2" />
            Clear
          </button>
        </div>
      </div>

      {/* Settings Panel */}
      {showSettings && (
        <div className="mb-4">
          <ChatSettings settings={settings} onChange={handleSettingsChange} />
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
            <p className="mt-1 text-sm text-red-700">{error}</p>
          </div>
          <button onClick={clearError} className="text-red-600 hover:text-red-800">
            ×
          </button>
        </div>
      )}

      {/* Chat Container */}
      <div className="flex-1 flex flex-col bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.length === 0 ? (
            <div className="flex items-center justify-center h-full">
              <div className="text-center max-w-md">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
                  <MessageSquare className="w-8 h-8 text-primary-600" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  Start a conversation
                </h3>
                <p className="text-gray-600 mb-6">
                  Ask questions about your documents and get AI-powered answers with source
                  citations.
                </p>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 text-left">
                  <h4 className="text-sm font-medium text-blue-900 mb-2">Example questions:</h4>
                  <ul className="text-sm text-blue-800 space-y-1">
                    <li>• "What are the main topics in my documents?"</li>
                    <li>• "Summarize the key points about climate change"</li>
                    <li>• "What does the document say about renewable energy?"</li>
                    <li>• "Find information about artificial intelligence"</li>
                  </ul>
                </div>
              </div>
            </div>
          ) : (
            <>
              <ChatMessages messages={messages} sources={sources} />
              <div ref={messagesEndRef} />
            </>
          )}
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4 bg-gray-50">
          <ChatInput
            onSend={handleSendMessage}
            disabled={isSending}
            placeholder="Ask a question about your documents..."
          />
          {isSending && (
            <div className="mt-2 flex items-center text-sm text-gray-600">
              <div className="spinner mr-2" />
              <span>Searching documents and generating response...</span>
            </div>
          )}
        </div>
      </div>

      {/* Message Count */}
      {messages.length > 0 && (
        <div className="mt-2 text-xs text-gray-500 text-center">
          {messages.length} message{messages.length !== 1 ? 's' : ''} in conversation
        </div>
      )}
    </div>
  );
};

export default ChatPageWithHook;
