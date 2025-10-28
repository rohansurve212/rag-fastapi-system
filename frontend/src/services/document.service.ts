/**
 * Document Service
 * 
 * Service for document upload, management, and retrieval operations
 */

import { apiService } from './api.service';
import type {
  DocumentUploadResponse,
  DocumentListResponse,
  DocumentDetails,
  DocumentMetadata,
} from '@/types';

class DocumentService {
  /**
   * Upload a document
   */
  async uploadDocument(
    file: File,
    onProgress?: (progress: number) => void
  ): Promise<DocumentUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await apiService.post<DocumentUploadResponse>(
      '/api/v1/documents/upload',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent: any) => {
          if (progressEvent.total && onProgress) {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            onProgress(percentCompleted);
          }
        },
      }
    );

    return response;
  }

  /**
   * Get list of all documents
   */
  async listDocuments(): Promise<DocumentListResponse> {
    return apiService.get<DocumentListResponse>('/api/v1/documents/');
  }

  /**
   * Get details of a specific document
   */
  async getDocument(documentId: string): Promise<DocumentDetails> {
    // Fetch document metadata
    const docResponse = await apiService.get<any>(`/api/v1/documents/${documentId}`);

    // Fetch document chunks
    const chunksResponse = await apiService.get<{ chunks: any[]; total_count: number }>(
      `/api/v1/documents/${documentId}/chunks`
    );

    // Combine into DocumentDetails
    return {
      ...docResponse.metadata,
      chunks: chunksResponse.chunks || [],
    };
  }

  /**
   * Delete a document
   */
  async deleteDocument(documentId: string): Promise<{ message: string; success: boolean }> {
    return apiService.delete(`/api/v1/documents/${documentId}`);
  }

  /**
   * Get document metadata by ID
   */
  async getDocumentMetadata(documentId: string): Promise<DocumentMetadata> {
    return apiService.get<DocumentMetadata>(`/api/v1/documents/${documentId}/metadata`);
  }

  /**
   * Validate file before upload
   */
  validateFile(file: File, maxSize: number, allowedTypes: string[]): { valid: boolean; error?: string } {
    // Check file size
    if (file.size > maxSize) {
      return {
        valid: false,
        error: `File size exceeds maximum allowed size of ${Math.round(maxSize / 1024 / 1024)}MB`,
      };
    }

    // Check file type
    const fileExtension = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!allowedTypes.includes(fileExtension)) {
      return {
        valid: false,
        error: `File type not allowed. Allowed types: ${allowedTypes.join(', ')}`,
      };
    }

    return { valid: true };
  }
}

export const documentService = new DocumentService();
export default documentService;
