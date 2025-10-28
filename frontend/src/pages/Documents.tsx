/**
 * Documents Page (Alternative with Custom Hook)
 * 
 * Complete document management using the useDocuments hook
 * This is an optional alternative to the main Documents.tsx
 */

import { useEffect, useState } from 'react';
import { Upload, RefreshCw, AlertCircle, FileText } from 'lucide-react';
import { useDocuments } from '@/hooks';
import LoadingSpinner from '@/components/LoadingSpinner';
import DocumentUpload from '@/components/DocumentUpload';
import DocumentList from '@/components/DocumentList';
import DocumentDetailsModal from '@/components/DocumentDetailsModal';
import type { DocumentDetails } from '@/types';

const DocumentsWithHook: React.FC = () => {
  const {
    documents,
    isLoading,
    error,
    loadDocuments,
    getDocument,
    deleteDocument,
    clearError,
  } = useDocuments();

  const [selectedDocument, setSelectedDocument] = useState<DocumentDetails | null>(null);
  const [showUploadModal, setShowUploadModal] = useState(false);
  const [showDetailsModal, setShowDetailsModal] = useState(false);

  useEffect(() => {
    loadDocuments();
  }, [loadDocuments]);

  const handleUploadSuccess = () => {
    setShowUploadModal(false);
    clearError();
  };

  const handleViewDocument = async (documentId: string) => {
    try {
      const details = await getDocument(documentId);
      setSelectedDocument(details);
      setShowDetailsModal(true);
    } catch (err) {
      // Error is handled by the hook
    }
  };

  const handleDeleteDocument = async (documentId: string, filename: string) => {
    if (!confirm(`Are you sure you want to delete "${filename}"? This action cannot be undone.`)) {
      return;
    }

    try {
      await deleteDocument(documentId);
    } catch (err) {
      // Error is handled by the hook
    }
  };

  if (isLoading && documents.length === 0) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner text="Loading documents..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Documents</h1>
          <p className="mt-1 text-sm text-gray-600">
            Manage your document collection ({documents.length} total)
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <button
            onClick={loadDocuments}
            className="btn btn-secondary inline-flex items-center"
            disabled={isLoading}
          >
            <RefreshCw className={`w-4 h-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Refresh
          </button>
          <button
            onClick={() => setShowUploadModal(true)}
            className="btn btn-primary inline-flex items-center"
          >
            <Upload className="w-4 h-4 mr-2" />
            Upload Document
          </button>
        </div>
      </div>

      {/* Error Message */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
          <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
          <div className="flex-1">
            <h3 className="text-sm font-medium text-red-800">Error</h3>
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
      {documents.length === 0 && !isLoading && (
        <div className="card text-center py-12">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
            <FileText className="w-8 h-8 text-blue-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900 mb-2">No documents yet</h3>
          <p className="text-gray-600 mb-6">
            Upload your first document to get started with the RAG system.
          </p>
          <button
            onClick={() => setShowUploadModal(true)}
            className="btn btn-primary inline-flex items-center"
          >
            <Upload className="w-4 h-4 mr-2" />
            Upload Document
          </button>
        </div>
      )}

      {/* Document List */}
      {documents.length > 0 && (
        <DocumentList
          documents={documents}
          onView={handleViewDocument}
          onDelete={handleDeleteDocument}
        />
      )}

      {/* Upload Modal */}
      {showUploadModal && (
        <DocumentUpload
          onSuccess={handleUploadSuccess}
          onClose={() => setShowUploadModal(false)}
        />
      )}

      {/* Document Details Modal */}
      {showDetailsModal && selectedDocument && (
        <DocumentDetailsModal
          document={selectedDocument}
          onClose={() => {
            setShowDetailsModal(false);
            setSelectedDocument(null);
          }}
        />
      )}
    </div>
  );
};

export default DocumentsWithHook;
