/**
 * DocumentUpload Component
 * 
 * Modal for uploading documents with drag-and-drop support
 */

import { useState, useRef, DragEvent } from 'react';
import { X, Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';
import { documentService } from '@/services';
import { config } from '@/config';
import { formatFileSize, parseErrorMessage } from '@/utils';

interface DocumentUploadProps {
  onSuccess: () => void;
  onClose: () => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onSuccess, onClose }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileSelect = (file: File) => {
    setError(null);
    
    // Validate file
    const validation = documentService.validateFile(
      file,
      config.upload.maxFileSize,
      config.upload.allowedFileTypes
    );

    if (!validation.valid) {
      setError(validation.error || 'Invalid file');
      return;
    }

    setSelectedFile(file);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);

    const file = e.dataTransfer.files[0];
    if (file) {
      handleFileSelect(file);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setIsUploading(true);
      setError(null);
      setUploadProgress(0);

      await documentService.uploadDocument(selectedFile, (progress) => {
        setUploadProgress(progress);
      });

      setSuccess(true);
      setTimeout(() => {
        onSuccess();
      }, 1500);
    } catch (err) {
      setError(parseErrorMessage(err));
      setIsUploading(false);
    }
  };

  const handleRemoveFile = () => {
    setSelectedFile(null);
    setError(null);
    setUploadProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Overlay */}
      <div className="fixed inset-0 bg-gray-900 bg-opacity-50" onClick={onClose} />

      {/* Modal */}
      <div className="flex min-h-screen items-center justify-center p-4">
        <div className="relative bg-white rounded-lg shadow-xl w-full max-w-lg">
          {/* Header */}
          <div className="flex items-center justify-between border-b border-gray-200 px-6 py-4">
            <h2 className="text-xl font-semibold text-gray-900">Upload Document</h2>
            <button
              onClick={onClose}
              className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
              disabled={isUploading}
            >
              <X className="w-5 h-5 text-gray-500" />
            </button>
          </div>

          {/* Content */}
          <div className="px-6 py-4 space-y-4">
            {/* Success Message */}
            {success && (
              <div className="bg-green-50 border border-green-200 rounded-lg p-4 flex items-start">
                <CheckCircle className="w-5 h-5 text-green-600 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <h3 className="text-sm font-medium text-green-800">Upload successful!</h3>
                  <p className="mt-1 text-sm text-green-700">
                    Your document has been uploaded and processed.
                  </p>
                </div>
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex items-start">
                <AlertCircle className="w-5 h-5 text-red-600 mt-0.5 mr-3 flex-shrink-0" />
                <div>
                  <h3 className="text-sm font-medium text-red-800">Upload failed</h3>
                  <p className="mt-1 text-sm text-red-700">{error}</p>
                </div>
              </div>
            )}

            {/* Drop Zone */}
            {!selectedFile && !success && (
              <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
                  isDragging
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-300 hover:border-gray-400'
                }`}
              >
                <Upload
                  className={`w-12 h-12 mx-auto mb-4 ${
                    isDragging ? 'text-primary-600' : 'text-gray-400'
                  }`}
                />
                <p className="text-sm text-gray-700 mb-2">
                  <button
                    type="button"
                    onClick={() => fileInputRef.current?.click()}
                    className="text-primary-600 hover:text-primary-700 font-medium"
                  >
                    Click to upload
                  </button>{' '}
                  or drag and drop
                </p>
                <p className="text-xs text-gray-500">
                  PDF or TXT files up to {formatFileSize(config.upload.maxFileSize)}
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  className="hidden"
                  accept={config.upload.allowedFileTypes.join(',')}
                  onChange={handleFileInputChange}
                />
              </div>
            )}

            {/* Selected File */}
            {selectedFile && !success && (
              <div className="border border-gray-200 rounded-lg p-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3">
                    <div className="p-2 bg-blue-100 rounded-lg">
                      <FileText className="w-5 h-5 text-blue-600" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 truncate">
                        {selectedFile.name}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {formatFileSize(selectedFile.size)}
                      </p>
                    </div>
                  </div>
                  {!isUploading && (
                    <button
                      onClick={handleRemoveFile}
                      className="p-1 hover:bg-gray-100 rounded transition-colors"
                    >
                      <X className="w-4 h-4 text-gray-500" />
                    </button>
                  )}
                </div>

                {/* Upload Progress */}
                {isUploading && (
                  <div className="mt-3">
                    <div className="flex items-center justify-between text-xs text-gray-600 mb-1">
                      <span>Uploading...</span>
                      <span>{uploadProgress}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                      <div
                        className="bg-primary-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${uploadProgress}%` }}
                      />
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Info */}
            {!selectedFile && !success && (
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p className="text-xs text-blue-800">
                  <strong>Supported formats:</strong> PDF and TXT files
                  <br />
                  <strong>Max file size:</strong> {formatFileSize(config.upload.maxFileSize)}
                  <br />
                  <strong>Processing:</strong> Files are automatically chunked and embedded
                </p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="flex items-center justify-end space-x-3 border-t border-gray-200 px-6 py-4">
            <button
              onClick={onClose}
              className="btn btn-secondary"
              disabled={isUploading}
            >
              {success ? 'Close' : 'Cancel'}
            </button>
            {selectedFile && !success && (
              <button
                onClick={handleUpload}
                className="btn btn-primary"
                disabled={isUploading}
              >
                {isUploading ? 'Uploading...' : 'Upload'}
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default DocumentUpload;
