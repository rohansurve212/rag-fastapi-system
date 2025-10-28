/**
 * DocumentList Component
 * 
 * Table view of all documents with actions
 */

import { FileText, Eye, Trash2 } from 'lucide-react';
import { formatFileSize, formatRelativeTime, getFileTypeIcon } from '@/utils';
import type { DocumentMetadata } from '@/types';

interface DocumentListProps {
  documents: DocumentMetadata[];
  onView: (documentId: string) => void;
  onDelete: (documentId: string, filename: string) => void;
}

const DocumentList: React.FC<DocumentListProps> = ({ documents, onView, onDelete }) => {
  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    if (ext === 'pdf') {
      return <FileText className="w-5 h-5 text-red-500" />;
    }
    return <FileText className="w-5 h-5 text-blue-500" />;
  };

  return (
    <div className="card overflow-hidden p-0">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Document
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Type
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Size
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Chunks
              </th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Uploaded
              </th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                Actions
              </th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {documents.map((doc) => (
              <tr key={doc.document_id} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">{getFileIcon(doc.filename)}</div>
                    <div className="ml-3">
                      <div className="text-sm font-medium text-gray-900">{doc.filename}</div>
                      <div className="text-xs text-gray-500">
                        {doc.character_count?.toLocaleString() || 0} characters
                      </div>
                    </div>
                  </div>
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="badge badge-gray uppercase">{doc.file_type}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {formatFileSize(doc.file_size)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap">
                  <span className="badge badge-primary">{doc.chunk_count || 0}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                  {formatRelativeTime(doc.uploaded_at)}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex items-center justify-end space-x-2">
                    <button
                      onClick={() => onView(doc.document_id)}
                      className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg transition-colors"
                      title="View details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDelete(doc.document_id, doc.filename)}
                      className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                      title="Delete document"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Mobile View */}
      <div className="lg:hidden divide-y divide-gray-200">
        {documents.map((doc) => (
          <div key={doc.document_id} className="p-4">
            <div className="flex items-start justify-between mb-2">
              <div className="flex items-start space-x-2">
                {getFileIcon(doc.filename)}
                <div>
                  <p className="text-sm font-medium text-gray-900">{doc.filename}</p>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className="badge badge-gray text-xs uppercase">{doc.file_type}</span>
                    <span className="text-xs text-gray-500">
                      {formatFileSize(doc.file_size)}
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <div className="flex items-center justify-between mt-3">
              <div className="text-xs text-gray-500">
                <span className="font-medium">{doc.chunk_count || 0}</span> chunks •{' '}
                {formatRelativeTime(doc.uploaded_at)}
              </div>
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => onView(doc.document_id)}
                  className="p-2 text-blue-600 hover:bg-blue-50 rounded-lg"
                >
                  <Eye className="w-4 h-4" />
                </button>
                <button
                  onClick={() => onDelete(doc.document_id, doc.filename)}
                  className="p-2 text-red-600 hover:bg-red-50 rounded-lg"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DocumentList;
