/**
 * DocumentDetailsModal Component
 * 
 * Modal to view document details and text chunks
 */

import { X, FileText, Calendar, Hash, Database } from 'lucide-react';
import { formatFileSize, formatDate, truncateText } from '@/utils';
import type { DocumentDetails } from '@/types';

interface DocumentDetailsModalProps {
  document: DocumentDetails;
  onClose: () => void;
}

const DocumentDetailsModal: React.FC<DocumentDetailsModalProps> = ({ document, onClose }) => {
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Overlay */}
      <div className="fixed inset-0 bg-gray-900 bg-opacity-50" onClick={onClose} />

      {/* Modal */}
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="relative bg-white rounded-lg shadow-xl w-full max-w-4xl max-h-[90vh] flex flex-col">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
            <div className="flex items-center space-x-3">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="w-5 h-5 text-blue-600" />
              </div>
              <div>
                <h2 className="text-xl font-semibold text-gray-900">{document.filename}</h2>
                <p className="text-sm text-gray-500">Document Details</p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>

          {/* Content */}
          <div className="flex-1 overflow-y-auto px-6 py-4">
            {/* Metadata Grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center text-gray-500 text-sm mb-1">
                  <FileText className="w-4 h-4 mr-1" />
                  File Type
                </div>
                <p className="text-lg font-semibold text-gray-900 uppercase">
                  {document.file_type}
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center text-gray-500 text-sm mb-1">
                  <Database className="w-4 h-4 mr-1" />
                  File Size
                </div>
                <p className="text-lg font-semibold text-gray-900">
                  {formatFileSize(document.file_size)}
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center text-gray-500 text-sm mb-1">
                  <Hash className="w-4 h-4 mr-1" />
                  Chunks
                </div>
                <p className="text-lg font-semibold text-gray-900">
                  {document.chunk_count || document.chunks?.length || 0}
                </p>
              </div>

              <div className="bg-gray-50 rounded-lg p-4">
                <div className="flex items-center text-gray-500 text-sm mb-1">
                  <Calendar className="w-4 h-4 mr-1" />
                  Uploaded
                </div>
                <p className="text-lg font-semibold text-gray-900">
                  {formatDate(document.uploaded_at, 'MMM d, yyyy')}
                </p>
              </div>
            </div>

            {/* Statistics */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
              <h3 className="text-sm font-medium text-blue-900 mb-2">Statistics</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div>
                  <span className="text-blue-700">Characters:</span>{' '}
                  <span className="font-medium text-blue-900">
                    {document.character_count?.toLocaleString() || 'N/A'}
                  </span>
                </div>
                <div>
                  <span className="text-blue-700">Words:</span>{' '}
                  <span className="font-medium text-blue-900">
                    {document.word_count?.toLocaleString() || 'N/A'}
                  </span>
                </div>
                <div>
                  <span className="text-blue-700">Pages:</span>{' '}
                  <span className="font-medium text-blue-900">
                    {document.page_count || 'N/A'}
                  </span>
                </div>
                <div>
                  <span className="text-blue-700">Document ID:</span>{' '}
                  <span className="font-mono text-xs text-blue-900">
                    {document.document_id.slice(0, 8)}...
                  </span>
                </div>
              </div>
            </div>

            {/* Chunks */}
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3">
                Text Chunks ({document.chunks?.length || 0})
              </h3>
              {document.chunks && document.chunks.length > 0 ? (
              <div className="space-y-3">
                {document.chunks.map((chunk, index) => (
                  <div
                    key={chunk.chunk_id}
                    className="border border-gray-200 rounded-lg p-4 hover:border-primary-300 transition-colors"
                  >
                    <div className="flex items-start justify-between mb-2">
                      <span className="badge badge-gray">Chunk {chunk.chunk_index + 1}</span>
                      <span className="text-xs text-gray-500 font-mono">
                        {chunk.chunk_id.slice(0, 12)}...
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">
                      {chunk.text.length > 300
                        ? truncateText(chunk.text, 300)
                        : chunk.text}
                    </p>
                    {chunk.text.length > 300 && (
                      <button className="text-xs text-primary-600 hover:text-primary-700 mt-2">
                        Show more
                      </button>
                    )}
                  </div>
                ))}
              </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <p>No chunks available for this document.</p>
                </div>
              )}
            </div>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-end border-t border-gray-200 px-6 py-4">
            <button onClick={onClose} className="btn btn-secondary">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentDetailsModal;
