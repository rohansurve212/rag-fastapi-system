/**
 * ChatMessages Component
 * 
 * Display chat messages with user/assistant styling and source citations
 */

import { useState } from 'react';
import { User, Bot, FileText, ExternalLink, ChevronDown, ChevronUp } from 'lucide-react';
import { copyToClipboard } from '@/utils';
import type { ChatMessage, SourceAttribution } from '@/types';

interface ChatMessagesProps {
  messages: ChatMessage[];
  sources?: SourceAttribution[];
}

const ChatMessages: React.FC<ChatMessagesProps> = ({ messages, sources = [] }) => {
  const [expandedSources, setExpandedSources] = useState<Set<string>>(new Set());

  const handleCopyMessage = async (content: string) => {
    const success = await copyToClipboard(content);
    if (success) {
      alert('Message copied to clipboard!');
    }
  };

  const toggleSourceExpanded = (chunkId: string) => {
    setExpandedSources((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(chunkId)) {
        newSet.delete(chunkId);
      } else {
        newSet.add(chunkId);
      }
      return newSet;
    });
  };

  return (
    <div className="space-y-4">
      {messages.map((message, index) => {
        const isUser = message.role === 'user';
        const isLastAssistant =
          message.role === 'assistant' && index === messages.length - 1;

        return (
          <div
            key={index}
            className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}
          >
            <div
              className={`flex items-start space-x-3 max-w-3xl ${
                isUser ? 'flex-row-reverse space-x-reverse' : ''
              }`}
            >
              {/* Avatar */}
              <div
                className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  isUser ? 'bg-primary-600' : 'bg-gray-700'
                }`}
              >
                {isUser ? (
                  <User className="w-5 h-5 text-white" />
                ) : (
                  <Bot className="w-5 h-5 text-white" />
                )}
              </div>

              {/* Message Bubble */}
              <div className="flex-1">
                <div
                  className={`rounded-lg px-4 py-3 ${
                    isUser
                      ? 'bg-primary-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">
                    {message.content}
                  </p>
                </div>

                {/* Copy Button */}
                <button
                  onClick={() => handleCopyMessage(message.content)}
                  className="mt-1 text-xs text-gray-500 hover:text-gray-700"
                >
                  Copy
                </button>

                {/* Sources (only for last assistant message) */}
                {!isUser && isLastAssistant && sources.length > 0 && (
                  <div className="mt-3 space-y-2">
                    <div className="flex items-center text-xs font-medium text-gray-700">
                      <FileText className="w-3 h-3 mr-1" />
                      Sources ({sources.length})
                    </div>
                    {sources.map((source, idx) => {
                      const isExpanded = expandedSources.has(source.chunk_id);
                      return (
                        <button
                          key={source.chunk_id}
                          onClick={() => toggleSourceExpanded(source.chunk_id)}
                          className="w-full bg-white border border-gray-200 rounded-lg p-3 text-xs hover:border-primary-300 hover:shadow-sm transition-all text-left cursor-pointer"
                        >
                          <div className="flex items-start justify-between mb-2">
                            <div className="flex-1">
                              <div className="font-medium text-gray-900 flex items-center">
                                <FileText className="w-3 h-3 mr-1" />
                                {source.filename}
                              </div>
                              <div className="text-gray-500 mt-0.5">
                                Chunk {source.chunk_index + 1}
                                {source.similarity_score && (
                                  <span className="ml-2">
                                    • Score: {(source.similarity_score * 100).toFixed(1)}%
                                  </span>
                                )}
                              </div>
                            </div>
                            <div className="flex items-center space-x-2">
                              <span className="badge badge-primary">#{idx + 1}</span>
                              {isExpanded ? (
                                <ChevronUp className="w-4 h-4 text-gray-500" />
                              ) : (
                                <ChevronDown className="w-4 h-4 text-gray-500" />
                              )}
                            </div>
                          </div>
                          <p
                            className={`text-gray-700 whitespace-pre-wrap ${
                              isExpanded ? '' : 'overflow-hidden'
                            }`}
                            style={
                              isExpanded
                                ? {}
                                : {
                                    display: '-webkit-box',
                                    WebkitLineClamp: 2,
                                    WebkitBoxOrient: 'vertical',
                                  }
                            }
                          >
                            {source.chunk_text}
                          </p>
                          {!isExpanded && source.chunk_text && source.chunk_text.length > 150 && (
                            <div className="text-primary-600 text-xs mt-1 font-medium">
                              Click to expand...
                            </div>
                          )}
                        </button>
                      );
                    })}
                  </div>
                )}
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default ChatMessages;
