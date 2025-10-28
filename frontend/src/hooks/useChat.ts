/**
 * useChat Hook
 * 
 * Custom hook for RAG chat operations with conversation management
 */

import { useState, useCallback } from 'react';
import { chatService } from '@/services';
import { parseErrorMessage } from '@/utils';
import type { ChatMessage, RAGChatRequest, RAGChatResponse, SourceAttribution } from '@/types';

interface UseChatReturn {
  messages: ChatMessage[];
  sources: SourceAttribution[];
  isSending: boolean;
  error: string | null;
  sendMessage: (
    message: string,
    options?: Partial<RAGChatRequest>
  ) => Promise<RAGChatResponse | null>;
  clearChat: () => void;
  clearError: () => void;
  exportChat: () => string;
}

export const useChat = (): UseChatReturn => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [sources, setSources] = useState<SourceAttribution[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (
      message: string,
      options?: Partial<RAGChatRequest>
    ): Promise<RAGChatResponse | null> => {
      if (!message.trim() || isSending) return null;

      const userMessage: ChatMessage = {
        role: 'user',
        content: message.trim(),
      };

      // Add user message immediately
      setMessages((prev) => [...prev, userMessage]);
      setError(null);

      try {
        setIsSending(true);

        // Get conversation history (exclude the message we just added)
        const conversationHistory = messages;

        const request: RAGChatRequest = {
          query: message.trim(),
          conversation_history: conversationHistory,
          top_k: options?.top_k ?? 5,
          search_type: options?.search_type ?? 'semantic',
          temperature: options?.temperature ?? 0.7,
          max_tokens: options?.max_tokens ?? 500,
          include_metadata: options?.include_metadata ?? true,
        };

        const response = await chatService.ragChat(request);

        const assistantMessage: ChatMessage = {
          role: 'assistant',
          content: response.response,
        };

        setMessages((prev) => [...prev, assistantMessage]);
        setSources(response.sources);

        return response;
      } catch (err) {
        const errorMsg = parseErrorMessage(err);
        setError(errorMsg);
        // Remove the user message on error
        setMessages((prev) => prev.slice(0, -1));
        return null;
      } finally {
        setIsSending(false);
      }
    },
    [messages, isSending]
  );

  const clearChat = useCallback(() => {
    setMessages([]);
    setSources([]);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const exportChat = useCallback((): string => {
    const exportText = messages
      .map((msg) => `${msg.role.toUpperCase()}: ${msg.content}`)
      .join('\n\n');

    const header =
      `RAG Chat Export\n` +
      `Date: ${new Date().toLocaleString()}\n` +
      `Messages: ${messages.length}\n` +
      `${'='.repeat(80)}\n\n`;

    return header + exportText;
  }, [messages]);

  return {
    messages,
    sources,
    isSending,
    error,
    sendMessage,
    clearChat,
    clearError,
    exportChat,
  };
};

export default useChat;
