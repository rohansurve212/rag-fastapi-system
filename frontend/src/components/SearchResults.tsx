/**
 * SearchResults Component
 * 
 * Display search results with score, highlighting, and actions
 */

import { FileText, X, Download, Copy, ExternalLink, Info } from 'lucide-react';
import { useState } from 'react';
import { formatFileSize, copyToClipboard, downloadTextFile } from '@/utils';
import type { SearchResponse } from '@/types';

interface SearchResultsProps {
  results: SearchResponse;
  query: string;
  onClear: () => void;
}

const SearchResults: React.FC<SearchResultsProps> = ({ results, query, onClear }) => {
  const [showScoreTooltip, setShowScoreTooltip] = useState<string | null>(null);

  const handleCopyResult = async (text: string) => {
    const success = await copyToClipboard(text);
    if (success) {
      alert('Copied to clipboard!');
    }
  };

  const handleExportResults = () => {
    const exportText = results.results
      .map(
        (result, index) =>
          `Result ${index + 1} (Relevance: ${result.score ? formatScore(result.score) : 'N/A'})\n` +
          `Document: ${result.filename}\n` +
          `Chunk: ${result.chunk_index + 1}\n` +
          `Text:\n${result.text}\n` +
          `${'-'.repeat(80)}\n`
      )
      .join('\n');

    const header = `Search Results for: "${query}"\n` +
      `Search Type: ${results.search_type}\n` +
      `Total Results: ${results.total_results}\n` +
      `Processing Time: ${results.processing_time_ms}ms\n` +
      `Timestamp: ${results.timestamp}\n` +
      `${'='.repeat(80)}\n\n`;

    downloadTextFile(
      header + exportText,
      `search-results-${new Date().getTime()}.txt`
    );
  };

  const highlightQuery = (text: string) => {
    if (!query) return text;
    
    const parts = text.split(new RegExp(`(${query})`, 'gi'));
    return parts.map((part, index) =>
      part.toLowerCase() === query.toLowerCase() ? (
        <mark key={index} className="bg-yellow-200 px-1 rounded">
          {part}
        </mark>
      ) : (
        part
      )
    );
  };

  const getScoreColor = (score: number) => {
    if (score >= 0.8) return 'text-green-700 bg-green-100 border-green-300';
    if (score >= 0.6) return 'text-blue-700 bg-blue-100 border-blue-300';
    if (score >= 0.4) return 'text-yellow-700 bg-yellow-100 border-yellow-300';
    if (score >= 0.2) return 'text-orange-700 bg-orange-100 border-orange-300';
    return 'text-gray-700 bg-gray-100 border-gray-300';
  };

  const formatScore = (score: number) => {
    // Convert to percentage for better readability
    const percentage = (score * 100).toFixed(1);
    return `${percentage}%`;
  };

  const getScoreDescription = (score: number) => {
    if (score >= 0.8) return 'Excellent match - This chunk is highly relevant to your query';
    if (score >= 0.6) return 'Good match - This chunk contains relevant information';
    if (score >= 0.4) return 'Moderate match - This chunk has some relevant content';
    if (score >= 0.2) return 'Weak match - This chunk has limited relevance';
    return 'Poor match - This chunk may not be very relevant';
  };

  return (
    <div className="space-y-4">
      {/* Results Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">
            Search Results
          </h2>
          <p className="text-sm text-gray-600 mt-1">
            Showing {results.results.length} of {results.total_results} results for{' '}
            <span className="font-medium">"{query}"</span>
          </p>
        </div>
        <div className="flex items-center space-x-2">
          <button
            onClick={handleExportResults}
            className="btn btn-secondary inline-flex items-center text-sm"
          >
            <Download className="w-4 h-4 mr-2" />
            Export
          </button>
          <button
            onClick={onClear}
            className="btn btn-secondary inline-flex items-center text-sm"
          >
            <X className="w-4 h-4 mr-2" />
            Clear
          </button>
        </div>
      </div>

      {/* Search Metadata */}
      <div className="card bg-blue-50 border-blue-200">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <span className="text-blue-700">Search Type:</span>{' '}
            <span className="font-medium text-blue-900 capitalize">{results.search_type}</span>
          </div>
          <div>
            <span className="text-blue-700">Results:</span>{' '}
            <span className="font-medium text-blue-900">{results.total_results}</span>
          </div>
          <div>
            <span className="text-blue-700">Processing Time:</span>{' '}
            <span className="font-medium text-blue-900">{results.processing_time_ms}ms</span>
          </div>
          <div>
            <span className="text-blue-700">Query:</span>{' '}
            <span className="font-medium text-blue-900 truncate">"{query}"</span>
          </div>
        </div>
      </div>

      {/* Results List */}
      <div className="space-y-4">
        {results.results.map((result, index) => (
          <div
            key={result.chunk_id}
            className="card hover:shadow-md transition-shadow"
          >
            {/* Result Header */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-start space-x-3 flex-1 min-w-0">
                <div className="flex-shrink-0 mt-1">
                  <div className="p-2 bg-blue-100 rounded-lg">
                    <FileText className="w-5 h-5 text-blue-600" />
                  </div>
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="text-base font-medium text-gray-900 truncate">
                    {result.filename}
                  </h3>
                  <div className="flex items-center space-x-3 mt-1 text-xs text-gray-500">
                    <span>Chunk {result.chunk_index + 1}</span>
                    <span>•</span>
                    <span className="font-mono">{result.chunk_id.slice(0, 12)}...</span>
                  </div>
                </div>
              </div>
              
              {/* Score Badge */}
              <div className="flex items-center space-x-2 flex-shrink-0 ml-3 relative">
                <span className={`badge px-3 py-1 border ${getScoreColor(result.score || 0)}`}>
                  {result.score ? formatScore(result.score) : 'N/A'}
                </span>
                {result.score !== undefined && (
                  <div className="relative">
                    <button
                      onMouseEnter={() => setShowScoreTooltip(result.chunk_id)}
                      onMouseLeave={() => setShowScoreTooltip(null)}
                      className="p-1 hover:bg-gray-200 rounded-full transition-colors"
                      aria-label="Score explanation"
                    >
                      <Info className="w-4 h-4 text-gray-500" />
                    </button>
                    {showScoreTooltip === result.chunk_id && (
                      <div className="absolute z-10 right-0 top-8 w-64 bg-gray-900 text-white text-xs rounded-lg p-3 shadow-lg">
                        <div className="font-semibold mb-1">Relevance Score</div>
                        <div className="text-gray-300">{getScoreDescription(result.score)}</div>
                        <div className="absolute -top-2 right-4 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-gray-900"></div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>

            {/* Result Text */}
            <div className="bg-gray-50 rounded-lg p-4 mb-3">
              <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
                {highlightQuery(result.text)}
              </p>
            </div>

            {/* Result Actions */}
            <div className="flex items-center justify-between pt-3 border-t border-gray-200">
              <div className="text-xs text-gray-500">
                Result #{index + 1}
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => handleCopyResult(result.text)}
                  className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Copy text"
                >
                  <Copy className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* No Results */}
      {results.results.length === 0 && (
        <div className="card text-center py-12">
          <div className="inline-flex items-center justify-center w-12 h-12 bg-gray-100 rounded-full mb-3">
            <FileText className="w-6 h-6 text-gray-400" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No results found</h3>
          <p className="text-gray-600">
            Try adjusting your search query or using different search filters.
          </p>
        </div>
      )}
    </div>
  );
};

export default SearchResults;
