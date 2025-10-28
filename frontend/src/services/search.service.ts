/**
 * Search Service
 * 
 * Service for all search operations: semantic, keyword, hybrid, and context search
 */

import { apiService } from './api.service';
import type { SearchRequest, SearchResponse, SearchStats } from '@/types';

class SearchService {
  /**
   * Transform backend search response to frontend format
   */
  private transformSearchResponse(backendResponse: any, startTime: number): SearchResponse {
    // Transform and sort results by score (highest first)
    const transformedResults = backendResponse.results.map((result: any) => ({
      chunk_id: result.chunk_id,
      document_id: result.document_id,
      filename: result.document_name || result.filename,
      text: result.text,
      // Handle different score field names from different search types
      score: result.similarity_score || result.combined_score || result.relevance_score || result.score || 0,
      chunk_index: result.chunk_index,
      metadata: result.metadata,
      highlights: result.highlights,
    }));

    // Sort by score in descending order (highest relevance first)
    transformedResults.sort((a, b) => (b.score || 0) - (a.score || 0));

    return {
      results: transformedResults,
      query: backendResponse.query,
      search_type: backendResponse.search_type,
      total_results: backendResponse.results_count || backendResponse.total_results || backendResponse.results.length,
      processing_time_ms: Date.now() - startTime,
      timestamp: backendResponse.timestamp,
    };
  }

  /**
   * Perform semantic search
   */
  async semanticSearch(query: string, topK: number = 5): Promise<SearchResponse> {
    const startTime = Date.now();
    const response = await apiService.get<any>('/api/v1/search/semantic', {
      query,
      top_k: topK,
    });
    return this.transformSearchResponse(response, startTime);
  }

  /**
   * Perform keyword search
   */
  async keywordSearch(query: string, topK: number = 5): Promise<SearchResponse> {
    const startTime = Date.now();
    const response = await apiService.get<any>('/api/v1/search/keyword', {
      query,
      top_k: topK,
    });
    return this.transformSearchResponse(response, startTime);
  }

  /**
   * Perform hybrid search (combines semantic and keyword)
   */
  async hybridSearch(
    query: string,
    topK: number = 5,
    rerank: boolean = false
  ): Promise<SearchResponse> {
    const startTime = Date.now();
    const response = await apiService.get<any>('/api/v1/search/hybrid', {
      query,
      top_k: topK,
      rerank,
    });
    return this.transformSearchResponse(response, startTime);
  }

  /**
   * Perform context search
   */
  async contextSearch(
    query: string,
    topK: number = 5,
    contextWindow: number = 1
  ): Promise<SearchResponse> {
    const startTime = Date.now();
    const response = await apiService.get<any>('/api/v1/search/context', {
      query,
      top_k: topK,
      context_window: contextWindow,
    });
    return this.transformSearchResponse(response, startTime);
  }

  /**
   * Get search statistics
   */
  async getSearchStats(): Promise<SearchStats> {
    return apiService.get<SearchStats>('/api/v1/search/stats');
  }

  /**
   * Generic search method that routes to appropriate search type
   */
  async search(request: SearchRequest): Promise<SearchResponse> {
    const { query, top_k = 5, search_type = 'semantic', rerank = false } = request;

    switch (search_type) {
      case 'semantic':
        return this.semanticSearch(query, top_k);
      case 'keyword':
        return this.keywordSearch(query, top_k);
      case 'hybrid':
        return this.hybridSearch(query, top_k, rerank);
      case 'context':
        return this.contextSearch(query, top_k);
      default:
        return this.semanticSearch(query, top_k);
    }
  }
}

export const searchService = new SearchService();
export default searchService;
