/**
 * useSearch Hook
 * 
 * Custom hook for search operations with state management
 */

import { useState, useCallback } from 'react';
import { searchService } from '@/services';
import { parseErrorMessage } from '@/utils';
import type { SearchRequest, SearchResponse, SearchStats } from '@/types';

interface UseSearchReturn {
  results: SearchResponse | null;
  stats: SearchStats | null;
  isSearching: boolean;
  error: string | null;
  search: (request: SearchRequest) => Promise<void>;
  semanticSearch: (query: string, topK?: number) => Promise<void>;
  keywordSearch: (query: string, topK?: number) => Promise<void>;
  hybridSearch: (query: string, topK?: number, rerank?: boolean) => Promise<void>;
  contextSearch: (query: string, topK?: number, contextWindow?: number) => Promise<void>;
  loadStats: () => Promise<void>;
  clearResults: () => void;
  clearError: () => void;
}

export const useSearch = (): UseSearchReturn => {
  const [results, setResults] = useState<SearchResponse | null>(null);
  const [stats, setStats] = useState<SearchStats | null>(null);
  const [isSearching, setIsSearching] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const search = useCallback(async (request: SearchRequest): Promise<void> => {
    try {
      setIsSearching(true);
      setError(null);
      const response = await searchService.search(request);
      setResults(response);
    } catch (err) {
      const errorMsg = parseErrorMessage(err);
      setError(errorMsg);
      setResults(null);
      throw err;
    } finally {
      setIsSearching(false);
    }
  }, []);

  const semanticSearch = useCallback(async (query: string, topK: number = 5): Promise<void> => {
    await search({ query, top_k: topK, search_type: 'semantic' });
  }, [search]);

  const keywordSearch = useCallback(async (query: string, topK: number = 5): Promise<void> => {
    await search({ query, top_k: topK, search_type: 'keyword' });
  }, [search]);

  const hybridSearch = useCallback(
    async (query: string, topK: number = 5, rerank: boolean = false): Promise<void> => {
      await search({ query, top_k: topK, search_type: 'hybrid', rerank });
    },
    [search]
  );

  const contextSearch = useCallback(
    async (query: string, topK: number = 5, contextWindow: number = 1): Promise<void> => {
      await search({ query, top_k: topK, search_type: 'context' });
    },
    [search]
  );

  const loadStats = useCallback(async (): Promise<void> => {
    try {
      setError(null);
      const response = await searchService.getSearchStats();
      setStats(response);
    } catch (err) {
      const errorMsg = parseErrorMessage(err);
      setError(errorMsg);
      throw err;
    }
  }, []);

  const clearResults = useCallback(() => {
    setResults(null);
    setError(null);
  }, []);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    results,
    stats,
    isSearching,
    error,
    search,
    semanticSearch,
    keywordSearch,
    hybridSearch,
    contextSearch,
    loadStats,
    clearResults,
    clearError,
  };
};

export default useSearch;
