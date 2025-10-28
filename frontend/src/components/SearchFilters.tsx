/**
 * SearchFilters Component
 * 
 * Advanced filters for search configuration
 */

import { Info } from 'lucide-react';
import type { SearchFilters as SearchFiltersType } from '@/types';

interface SearchFiltersProps {
  filters: SearchFiltersType;
  onChange: (filters: Partial<SearchFiltersType>) => void;
  onSearch: () => void;
}

const searchTypeOptions = [
  {
    value: 'semantic' as const,
    label: 'Semantic Search',
    description: 'Find conceptually similar content using AI embeddings',
  },
  {
    value: 'keyword' as const,
    label: 'Keyword Search',
    description: 'Traditional text-based search for exact matches',
  },
  {
    value: 'hybrid' as const,
    label: 'Hybrid Search',
    description: 'Combines semantic and keyword search for best results',
  },
  {
    value: 'context' as const,
    label: 'Context Search',
    description: 'Returns results with surrounding text for better context',
  },
];

const SearchFilters: React.FC<SearchFiltersProps> = ({ filters, onChange, onSearch }) => {
  return (
    <div className="card bg-gray-50">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Search Filters</h3>

      <div className="space-y-6">
        {/* Search Type */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Search Type
          </label>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {searchTypeOptions.map((option) => (
              <button
                key={option.value}
                onClick={() => onChange({ searchType: option.value })}
                className={`p-4 rounded-lg border-2 text-left transition-all ${
                  filters.searchType === option.value
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 bg-white hover:border-gray-300'
                }`}
              >
                <div className="flex items-start justify-between mb-1">
                  <span className="font-medium text-gray-900">{option.label}</span>
                  {filters.searchType === option.value && (
                    <div className="w-2 h-2 bg-primary-600 rounded-full" />
                  )}
                </div>
                <p className="text-xs text-gray-600">{option.description}</p>
              </button>
            ))}
          </div>
        </div>

        {/* Number of Results */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Number of Results: <span className="text-primary-600">{filters.topK}</span>
          </label>
          <input
            type="range"
            min="1"
            max="20"
            value={filters.topK}
            onChange={(e) => onChange({ topK: parseInt(e.target.value) })}
            className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>1</span>
            <span>10</span>
            <span>20</span>
          </div>
        </div>

        {/* Rerank Option (for hybrid search) */}
        {filters.searchType === 'hybrid' && (
          <div>
            <label className="flex items-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={filters.rerank}
                onChange={(e) => onChange({ rerank: e.target.checked })}
                className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <div>
                <span className="text-sm font-medium text-gray-900">
                  Enable Reranking
                </span>
                <p className="text-xs text-gray-600">
                  Reorder results for better relevance (may take longer)
                </p>
              </div>
            </label>
          </div>
        )}

        {/* Info Box */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-start">
          <Info className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
          <div className="text-sm text-blue-800">
            <strong>Tip:</strong> Use semantic search for conceptual queries and keyword search
            for finding specific terms. Hybrid search combines both for comprehensive results.
          </div>
        </div>

        {/* Apply Button */}
        <button onClick={onSearch} className="btn btn-primary w-full">
          Apply Filters
        </button>
      </div>
    </div>
  );
};

export default SearchFilters;
