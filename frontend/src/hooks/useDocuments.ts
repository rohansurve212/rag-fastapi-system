/**
 * useDocuments Hook
 * 
 * Custom hook for document operations with state management
 */

import { useState, useCallback } from 'react';
import { documentService } from '@/services';
import { parseErrorMessage } from '@/utils';
import type { DocumentMetadata, DocumentDetails, DocumentUploadResponse } from '@/types';

interface UseDocumentsReturn {
  documents: DocumentMetadata[];
  isLoading: boolean;
  error: string | null;
  loadDocuments: () => Promise<void>;
  uploadDocument: (file: File, onProgress?: (progress: number) => void) => Promise<DocumentUploadResponse>;
  getDocument: (documentId: string) => Promise<DocumentDetails>;
  deleteDocument: (documentId: string) => Promise<void>;
  clearError: () => void;
}

export const useDocuments = (): UseDocumentsReturn => {
  const [documents, setDocuments] = useState<DocumentMetadata[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const loadDocuments = useCallback(async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await documentService.listDocuments();
      setDocuments(response.documents);
    } catch (err) {
      const errorMsg = parseErrorMessage(err);
      setError(errorMsg);
      throw err;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const uploadDocument = useCallback(async (
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<DocumentUploadResponse> => {
    try {
      setError(null);
      const response = await documentService.uploadDocument(file, onProgress);
      // Reload documents after successful upload
      await loadDocuments();
      return response;
    } catch (err) {
      const errorMsg = parseErrorMessage(err);
      setError(errorMsg);
      throw err;
    }
  }, [loadDocuments]);

  const getDocument = useCallback(async (documentId: string): Promise<DocumentDetails> => {
    try {
      setError(null);
      return await documentService.getDocument(documentId);
    } catch (err) {
      const errorMsg = parseErrorMessage(err);
      setError(errorMsg);
      throw err;
    }
  }, []);

  const deleteDocument = useCallback(async (documentId: string): Promise<void> => {
    try {
      setError(null);
      await documentService.deleteDocument(documentId);
      // Reload documents after successful deletion
      await loadDocuments();
    } catch (err) {
      const errorMsg = parseErrorMessage(err);
      setError(errorMsg);
      throw err;
    }
  }, [loadDocuments]);

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  return {
    documents,
    isLoading,
    error,
    loadDocuments,
    uploadDocument,
    getDocument,
    deleteDocument,
    clearError,
  };
};

export default useDocuments;
