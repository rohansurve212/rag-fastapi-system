/**
 * Health Page
 * 
 * System health and status monitoring
 */

import { useEffect, useState } from 'react';
import { CheckCircle2, XCircle, AlertCircle, RefreshCw } from 'lucide-react';
import { healthService } from '@/services';
import LoadingSpinner from '@/components/LoadingSpinner';
import type { APIStatusResponse, RAGHealthResponse } from '@/types';

const Health: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<APIStatusResponse | null>(null);
  const [ragHealth, setRagHealth] = useState<RAGHealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState<Date>(new Date());

  useEffect(() => {
    loadHealthData();
  }, []);

  const loadHealthData = async () => {
    try {
      setIsLoading(true);
      const [apiRes, ragRes] = await Promise.all([
        healthService.getAPIStatus(),
        healthService.checkRAGHealth(),
      ]);
      setApiStatus(apiRes);
      setRagHealth(ragRes);
      setLastChecked(new Date());
    } catch (error) {
      console.error('Failed to load health data:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusIcon = (status: boolean) => {
    return status ? (
      <CheckCircle2 className="w-5 h-5 text-green-500" />
    ) : (
      <XCircle className="w-5 h-5 text-red-500" />
    );
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner text="Checking system health..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">System Health</h1>
          <p className="mt-1 text-sm text-gray-600">
            Monitor system status and performance
          </p>
        </div>
        <button
          onClick={loadHealthData}
          className="btn btn-secondary inline-flex items-center"
        >
          <RefreshCw className="w-4 h-4 mr-2" />
          Refresh
        </button>
      </div>

      {/* Last Checked */}
      <div className="text-sm text-gray-500">
        Last checked: {lastChecked.toLocaleTimeString()}
      </div>

      {/* API Status */}
      {apiStatus && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">API Status</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">Version</span>
              <span className="badge badge-primary">{apiStatus.api_version}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">Status</span>
              <span className="badge badge-success capitalize">{apiStatus.status}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">OpenAI Configured</span>
              {getStatusIcon(apiStatus.openai_status.configured)}
            </div>
            {apiStatus.openai_status.configured && (
              <>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">Chat Model</span>
                  <span className="text-sm font-mono text-gray-900">
                    {apiStatus.openai_status.model}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-700">Embedding Model</span>
                  <span className="text-sm font-mono text-gray-900">
                    {apiStatus.openai_status.embedding_model}
                  </span>
                </div>
              </>
            )}
          </div>
        </div>
      )}

      {/* RAG System Health */}
      {ragHealth && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">RAG System Health</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">Overall Status</span>
              <span
                className={`badge ${
                  ragHealth.status === 'healthy' ? 'badge-success' : 'badge-warning'
                } capitalize`}
              >
                {ragHealth.status}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">Database Connection</span>
              {getStatusIcon(ragHealth.database_connection)}
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">OpenAI Configured</span>
              {getStatusIcon(ragHealth.openai_configured)}
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-gray-700">Embeddings Ready</span>
              {getStatusIcon(ragHealth.embedding_ready)}
            </div>
          </div>
        </div>
      )}

      {/* Statistics */}
      {ragHealth && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Total Documents</p>
            <p className="text-3xl font-bold text-gray-900">{ragHealth.total_documents}</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Total Chunks</p>
            <p className="text-3xl font-bold text-gray-900">{ragHealth.total_chunks}</p>
          </div>
          <div className="card">
            <p className="text-sm text-gray-600 mb-1">Indexed Chunks</p>
            <p className="text-3xl font-bold text-gray-900">{ragHealth.indexed_chunks}</p>
          </div>
        </div>
      )}

      {/* Available Endpoints */}
      {apiStatus && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Available Endpoints</h2>
          <div className="space-y-2 max-h-96 overflow-y-auto">
            {Object.entries(apiStatus.endpoints).map(([name, path]) => (
              <div
                key={name}
                className="flex items-center justify-between py-2 px-3 bg-gray-50 rounded"
              >
                <span className="text-sm text-gray-700">{name}</span>
                <code className="text-xs font-mono text-gray-600">{path}</code>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Health;
