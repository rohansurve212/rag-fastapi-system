/**
 * ChatSettings Component
 * 
 * Configuration panel for RAG chat parameters
 */

import { Info } from 'lucide-react';

interface ChatSettings {
  topK: number;
  searchType: 'semantic' | 'keyword' | 'hybrid' | 'context';
  temperature: number;
  maxTokens: number;
  includeMetadata: boolean;
}

interface ChatSettingsProps {
  settings: ChatSettings;
  onChange: (settings: Partial<ChatSettings>) => void;
}

const searchTypeOptions = [
  {
    value: 'semantic' as const,
    label: 'Semantic',
    description: 'AI-powered conceptual search',
  },
  {
    value: 'keyword' as const,
    label: 'Keyword',
    description: 'Traditional text matching',
  },
  {
    value: 'hybrid' as const,
    label: 'Hybrid',
    description: 'Combined semantic + keyword',
  },
  {
    value: 'context' as const,
    label: 'Context',
    description: 'With surrounding text',
  },
];

const ChatSettings: React.FC<ChatSettingsProps> = ({ settings, onChange }) => {
  return (
    <div className="card bg-gray-50">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Chat Settings</h3>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Left Column */}
        <div className="space-y-4">
          {/* Search Type */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Search Type
            </label>
            <div className="grid grid-cols-2 gap-2">
              {searchTypeOptions.map((option) => (
                <button
                  key={option.value}
                  onClick={() => onChange({ searchType: option.value })}
                  className={`p-3 rounded-lg border-2 text-left transition-all ${
                    settings.searchType === option.value
                      ? 'border-primary-500 bg-primary-50'
                      : 'border-gray-200 bg-white hover:border-gray-300'
                  }`}
                >
                  <div className="font-medium text-sm text-gray-900">{option.label}</div>
                  <div className="text-xs text-gray-600 mt-0.5">{option.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Number of Sources */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Sources: <span className="text-primary-600">{settings.topK}</span>
            </label>
            <input
              type="range"
              min="1"
              max="10"
              value={settings.topK}
              onChange={(e) => onChange({ topK: parseInt(e.target.value) })}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>1</span>
              <span>5</span>
              <span>10</span>
            </div>
          </div>
        </div>

        {/* Right Column */}
        <div className="space-y-4">
          {/* Temperature */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Temperature: <span className="text-primary-600">{settings.temperature}</span>
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={settings.temperature}
              onChange={(e) => onChange({ temperature: parseFloat(e.target.value) })}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0.0 (Focused)</span>
              <span>1.0 (Creative)</span>
            </div>
          </div>

          {/* Max Tokens */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Max Response Length: <span className="text-primary-600">{settings.maxTokens}</span>
            </label>
            <input
              type="range"
              min="100"
              max="1000"
              step="50"
              value={settings.maxTokens}
              onChange={(e) => onChange({ maxTokens: parseInt(e.target.value) })}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-600"
            />
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>100</span>
              <span>500</span>
              <span>1000</span>
            </div>
          </div>

          {/* Include Metadata */}
          <div>
            <label className="flex items-center space-x-2 cursor-pointer">
              <input
                type="checkbox"
                checked={settings.includeMetadata}
                onChange={(e) => onChange({ includeMetadata: e.target.checked })}
                className="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
              />
              <div>
                <span className="text-sm font-medium text-gray-900">Include Metadata</span>
                <p className="text-xs text-gray-600">Show source metadata with responses</p>
              </div>
            </label>
          </div>
        </div>
      </div>

      {/* Info Box */}
      <div className="mt-4 bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-start">
        <Info className="w-5 h-5 text-blue-600 mt-0.5 mr-2 flex-shrink-0" />
        <div className="text-sm text-blue-800">
          <strong>Tip:</strong> Higher temperature (0.7-1.0) generates more creative responses,
          while lower temperature (0.0-0.3) produces more focused answers. More sources provide
          better context but may slow down responses.
        </div>
      </div>
    </div>
  );
};

export default ChatSettings;
