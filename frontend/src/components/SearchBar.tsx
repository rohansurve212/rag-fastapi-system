/**
 * SearchBar Component
 * 
 * Search input with submit button and loading state
 */

import { useState, KeyboardEvent } from 'react';
import { Search, Loader2 } from 'lucide-react';

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
  onSearch: (query: string) => void;
  isSearching?: boolean;
  placeholder?: string;
}

const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  onSearch,
  isSearching = false,
  placeholder = 'Search...',
}) => {
  const handleKeyPress = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !isSearching) {
      onSearch(value);
    }
  };

  const handleSubmit = () => {
    if (!isSearching) {
      onSearch(value);
    }
  };

  return (
    <div className="card">
      <div className="flex items-center space-x-3">
        <div className="flex-1 relative">
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="w-5 h-5 text-gray-400" />
          </div>
          <input
            type="text"
            value={value}
            onChange={(e) => onChange(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={placeholder}
            disabled={isSearching}
            className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 disabled:bg-gray-50 disabled:text-gray-500"
          />
        </div>
        <button
          onClick={handleSubmit}
          disabled={isSearching || !value.trim()}
          className="btn btn-primary px-8 py-3 inline-flex items-center"
        >
          {isSearching ? (
            <>
              <Loader2 className="w-5 h-5 mr-2 animate-spin" />
              Searching...
            </>
          ) : (
            <>
              <Search className="w-5 h-5 mr-2" />
              Search
            </>
          )}
        </button>
      </div>
    </div>
  );
};

export default SearchBar;
