/**
 * Type Definitions
 * 
 * All TypeScript types and interfaces for the application.
 * These match the Pydantic models from the FastAPI backend.
 */

// ==================== Chat Types ====================

export interface ChatMessage {
  role: 'user' | 'assistant' | 'system';
  content: string;
}

export interface ChatRequest {
  message: string;
  conversation_history?: ChatMessage[];
  temperature?: number;
  max_tokens?: number;
}

export interface ChatResponse {
  response: string;
  message_count: number;
  tokens_used?: number;
  model: string;
  timestamp: string;
}

// ==================== RAG Types ====================

export interface RAGChatRequest {
  query: string;
  conversation_history?: ChatMessage[];
  top_k?: number;
  search_type?: 'semantic' | 'keyword' | 'hybrid';
  temperature?: number;
  max_tokens?: number;
  include_metadata?: boolean;
}

export interface SourceAttribution {
  chunk_id: string;
  document_id: string;
  filename: string;
  chunk_text: string;
  similarity_score?: number;
  chunk_index: number;
  metadata?: Record<string, any>;
}

export interface RAGChatResponse {
  response: string;
  sources: SourceAttribution[];
  message_count: number;
  tokens_used?: number;
  model: string;
  search_results_count: number;
  timestamp: string;
}

// ==================== Document Types ====================

export interface DocumentMetadata {
  document_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  file_hash: string;
  character_count?: number;
  word_count?: number;
  page_count?: number;
  chunk_count?: number;
  uploaded_at: string;
}

export interface DocumentUploadResponse {
  success: boolean;
  message: string;
  document_id: string;
  filename: string;
  file_size: number;
  file_hash: string;
  chunks_created: number;
  metadata: DocumentMetadata;
  timestamp: string;
}

export interface DocumentListResponse {
  documents: DocumentMetadata[];
  total_count: number;
  timestamp: string;
}

export interface DocumentDetails extends DocumentMetadata {
  document_id: string;
  chunks: ChunkData[];
}

// ==================== Search Types ====================

export interface SearchRequest {
  query: string;
  top_k?: number;
  search_type?: 'semantic' | 'keyword' | 'hybrid' | 'context';
  rerank?: boolean;
  document_ids?: string[];
}

export interface SearchResult {
  chunk_id: string;
  document_id: string;
  filename: string;
  text: string;
  score: number;
  chunk_index: number;
  metadata?: Record<string, any>;
  highlights?: string[];
}

export interface SearchResponse {
  results: SearchResult[];
  query: string;
  search_type: string;
  total_results: number;
  processing_time_ms: number;
  timestamp: string;
}

export interface SearchStats {
  total_documents: number;
  total_chunks: number;
  total_embeddings: number;
  average_chunks_per_document: number;
  document_types: Record<string, number>;
  timestamp: string;
}

// ==================== Chunk Types ====================

export interface ChunkData {
  chunk_id: string;
  text: string;
  chunk_index: number;
  document_id: string;
  metadata?: Record<string, any>;
}

// ==================== Health & Status Types ====================

export interface HealthResponse {
  status: 'healthy' | 'degraded' | 'unhealthy';
  timestamp: string;
  service: string;
  openai_configured: boolean;
}

export interface OpenAIStatus {
  configured: boolean;
  model?: string;
  embedding_model?: string;
}

export interface APIStatusResponse {
  api_version: string;
  status: string;
  timestamp: string;
  endpoints: Record<string, string>;
  openai_status: OpenAIStatus;
}

export interface RAGHealthResponse {
  status: string;
  database_connection: boolean;
  openai_configured: boolean;
  embedding_ready: boolean;
  total_documents: number;
  total_chunks: number;
  indexed_chunks: number;
  timestamp: string;
}

// ==================== Error Types ====================

export interface ErrorResponse {
  error: string;
  message: string;
  detail?: string;
  timestamp: string;
}

export interface APIError extends Error {
  response?: {
    data: ErrorResponse;
    status: number;
  };
}

// ==================== UI State Types ====================

export interface LoadingState {
  isLoading: boolean;
  message?: string;
}

export interface ErrorState {
  hasError: boolean;
  error?: Error | APIError;
  message?: string;
}

// ==================== Pagination Types ====================

export interface PaginationParams {
  page: number;
  pageSize: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// ==================== Filter Types ====================

export interface DocumentFilters {
  fileType?: string;
  dateFrom?: string;
  dateTo?: string;
  searchTerm?: string;
}

export interface SearchFilters {
  topK: number;
  searchType: 'semantic' | 'keyword' | 'hybrid' | 'context';
  rerank: boolean;
  documentIds?: string[];
}
