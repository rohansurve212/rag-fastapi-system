/**
 * Chat Service
 * 
 * Service for chat operations: simple chat and RAG-powered chat
 */

import { apiService } from './api.service';
import type {
  ChatRequest,
  ChatResponse,
  RAGChatRequest,
  RAGChatResponse,
} from '@/types';

class ChatService {
  /**
   * Send a simple chat message (no RAG)
   */
  async chat(request: ChatRequest): Promise<ChatResponse> {
    return apiService.post<ChatResponse>('/api/v1/chat', request);
  }

  /**
   * Test OpenAI connection
   */
  async testOpenAI(): Promise<ChatResponse> {
    return apiService.get<ChatResponse>('/api/v1/chat/test');
  }

  /**
   * Send a RAG-powered chat message
   */
  async ragChat(request: RAGChatRequest): Promise<RAGChatResponse> {
    const backendResponse = await apiService.post<any>('/api/v1/rag/chat', request);

    // Transform backend response to frontend format
    return {
      response: backendResponse.answer, // Backend uses 'answer', frontend expects 'response'
      sources: (backendResponse.sources || []).map((source: any) => ({
        chunk_id: source.chunk_id || `chunk_${source.document_id}_${source.chunk_index}`,
        document_id: source.document_id,
        filename: source.document_name || source.filename,
        chunk_text: source.text_preview || source.chunk_text || '',
        similarity_score: source.relevance_score || source.similarity_score,
        chunk_index: source.chunk_index,
        metadata: source.metadata,
      })),
      message_count: backendResponse.conversation_history?.length || 0,
      tokens_used: backendResponse.tokens_used,
      model: backendResponse.model,
      search_results_count: backendResponse.context_used || 0,
      timestamp: backendResponse.timestamp,
    };
  }

  /**
   * Create a chat request object with defaults
   */
  createChatRequest(
    message: string,
    options?: Partial<ChatRequest>
  ): ChatRequest {
    return {
      message,
      conversation_history: options?.conversation_history || [],
      temperature: options?.temperature ?? 0.7,
      max_tokens: options?.max_tokens ?? 500,
    };
  }

  /**
   * Create a RAG chat request object with defaults
   */
  createRAGChatRequest(
    query: string,
    options?: Partial<RAGChatRequest>
  ): RAGChatRequest {
    return {
      query,
      conversation_history: options?.conversation_history || [],
      top_k: options?.top_k ?? 5,
      search_type: options?.search_type ?? 'semantic',
      temperature: options?.temperature ?? 0.7,
      max_tokens: options?.max_tokens ?? 500,
      include_metadata: options?.include_metadata ?? true,
    };
  }
}

export const chatService = new ChatService();
export default chatService;
