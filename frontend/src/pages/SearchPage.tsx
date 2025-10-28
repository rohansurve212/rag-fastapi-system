/**
 * Search Page (Alternative with Custom Hook)
 * 
 * Complete search interface using the useSearch hook
 * This is an optional alternative to the main SearchPage.tsx
 */

import { useState } from 'react';
import { Search, SlidersHorizontal, AlertCircle } from 'lucide-react';
import { useSearch } from '@/hooks';
import SearchBar from '@/components/SearchBar';
import SearchFilters from '@/components/SearchFilters';
import SearchResults from '@/components/SearchResults';
import type { SearchFilters as SearchFiltersType } from '@/types';

const SearchPageWithHook: React.FC = () => {
  const {
    results,
    isSearching,
    error,
    search,
    clearResults,
    clearError,
  } = useSearch();

  const [query, setQuery] = useState('');
  const [showFilters, setShowFilters] = useState(false);
  const [filters, setFilters] = useState<SearchFiltersType>({
    topK: 5,
    searchType: 'semantic',
    rerank: false,
  });

  const handleSearch = async (searchQuery?: string) => {
    const q = searchQuery || query;
    
    if (!q.trim()) {
      return;
    }

    try {
      await search({
        query: q,
        top_k: filters.topK,
        search_type: filters.searchType,
        rerank: filters.rerank,
      });
    } catch (err) {
      // Error is handled by the hook
    }
  };

  const handleFilterChange = (newFilters: Partial<SearchFiltersType>) => {
    setFilters({ ...filters, ...newFilters });
  };

  const handleClearResults = () => {
    clearResults();
    setQuery('');
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Search Documents</h1>
        <p className="mt-1 text-sm text-gray-600">
          Find relevant information across all your documents
        </p>
      </div>

      {/* Search Bar */}
      <SearchBar
        value={query}
        onChange={setQuery}
        onSearch={handleSearch}
        isSearching={isSearching}
        placeholder="Search your documents..."
      />

      {/* Filters Toggle */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => setShowFilters(!showFilters)}
          className="btn btn-secondary inline-flex items-center text-sm"
        >
          <SlidersHorizontal className="w-4 h-4 mr-2" />
          {showFilters ? 'Hide' : 'Show'} Filters
        </button>

        {results && (
          <div className="text-sm text-gray-600">
            Found <span className="font-semibold">{results.total_results}</span> results in{' '}
            <span className="font-semibold">{results.processing_time_ms}ms</span>
          </div>
        )}
      </div>

      {/* Search Filters */}
      {showFilters && (
        <SearchFilters
          filters={filters}
          onChange={handleFilterChange}
          onSearch={() => handleSearch()}
        />
      )}

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="text-sm font-medium text-red-800">Search Error</h3>
            <p className="mt-1 text-sm text-red-700">{error}</p>
          </div>
          <button
            onClick={clearError}
            className="text-red-600 hover:text-red-800"
          >
            ×
          </button>
        </div>
      )}

      {/* Empty State */}
      {!results && !error && !isSearching && (
        <div className="card text-center py-16">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 rounded-full mb-4">
            <Search className="w-8 h-8 text-primary-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">
            Start searching your documents
          </h3>
          <p className="text-gray-600 mb-6 max-w-md mx-auto">
            Enter a search query above to find relevant information. You can use semantic search
            to find conceptually similar content or keyword search for exact matches.
          </p>
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 max-w-2xl mx-auto text-left">
            <h4 className="text-sm font-medium text-blue-900 mb-2">Search Tips:</h4>
            <ul className="text-sm text-blue-800 space-y-1">
              <li>• <strong>Semantic:</strong> Finds conceptually similar content (e.g., "climate change" finds "global warming")</li>
              <li>• <strong>Keyword:</strong> Searches for exact word matches in documents</li>
              <li>• <strong>Hybrid:</strong> Combines both semantic and keyword search</li>
              <li>• <strong>Context:</strong> Returns results with surrounding text for better understanding</li>
            </ul>
          </div>
        </div>
      )}

      {/* Search Results */}
      {results && (
        <SearchResults
          results={results}
          query={query}
          onClear={handleClearResults}
        />
      )}
    </div>
  );
};

export default SearchPageWithHook;
