/**
 * Dashboard Page
 * 
 * Main landing page with quick stats and actions
 */

import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import {
  FileText,
  Search,
  MessageSquare,
  Upload,
  TrendingUp,
  Database,
} from 'lucide-react';
import { searchService } from '@/services';
import LoadingSpinner from '@/components/LoadingSpinner';
import type { SearchStats } from '@/types';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState<SearchStats | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      setIsLoading(true);
      const response = await searchService.getSearchStats();
      setStats(response);
    } catch (error) {
      console.error('Failed to load stats:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const quickActions = [
    {
      name: 'Upload Document',
      description: 'Add new documents to your knowledge base',
      href: '/documents',
      icon: Upload,
      color: 'bg-blue-500',
    },
    {
      name: 'Search Documents',
      description: 'Find relevant information quickly',
      href: '/search',
      icon: Search,
      color: 'bg-green-500',
    },
    {
      name: 'Chat with RAG',
      description: 'Ask questions about your documents',
      href: '/chat',
      icon: MessageSquare,
      color: 'bg-purple-500',
    },
  ];

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <LoadingSpinner text="Loading dashboard..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-lg shadow-lg p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">Welcome to RAG System</h1>
        <p className="text-primary-100 text-lg">
          Intelligent document search and question answering powered by AI
        </p>
      </div>

      {/* Stats Grid */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-blue-100 rounded-lg">
                <FileText className="w-6 h-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Total Documents</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {stats.total_documents}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-green-100 rounded-lg">
                <Database className="w-6 h-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Total Chunks</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.total_chunks}</p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-purple-100 rounded-lg">
                <TrendingUp className="w-6 h-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Embeddings</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {stats.total_embeddings}
                </p>
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center">
              <div className="p-3 bg-yellow-100 rounded-lg">
                <FileText className="w-6 h-6 text-yellow-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm text-gray-600">Avg Chunks/Doc</p>
                <p className="text-2xl font-semibold text-gray-900">
                  {stats.average_chunks_per_document?.toFixed(1) || '0.0'}
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div>
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Link
                key={action.name}
                to={action.href}
                className="card hover:shadow-md transition-shadow group"
              >
                <div className="flex items-start">
                  <div className={`p-3 ${action.color} rounded-lg`}>
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                  <div className="ml-4 flex-1">
                    <h3 className="text-lg font-medium text-gray-900 group-hover:text-primary-600 transition-colors">
                      {action.name}
                    </h3>
                    <p className="mt-1 text-sm text-gray-600">{action.description}</p>
                  </div>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Getting Started */}
      {stats && stats.total_documents === 0 && (
        <div className="card bg-blue-50 border-blue-200">
          <div className="flex items-start">
            <div className="flex-shrink-0">
              <div className="p-2 bg-blue-100 rounded-lg">
                <FileText className="w-5 h-5 text-blue-600" />
              </div>
            </div>
            <div className="ml-3">
              <h3 className="text-sm font-medium text-blue-900">Get Started</h3>
              <p className="mt-1 text-sm text-blue-700">
                Upload your first document to start using the RAG system. You can upload PDF and
                text files.
              </p>
              <div className="mt-3">
                <Link to="/documents" className="btn btn-primary text-sm">
                  Upload Document
                </Link>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Document Types */}
      {stats && stats.total_documents > 0 && (
        <div className="card">
          <h3 className="text-lg font-medium text-gray-900 mb-4">Document Types</h3>
          <div className="space-y-3">
            {Object.entries(stats.document_types).map(([type, count]) => (
              <div key={type} className="flex items-center justify-between">
                <div className="flex items-center">
                  <FileText className="w-5 h-5 text-gray-400 mr-2" />
                  <span className="text-sm text-gray-700 capitalize">{type}</span>
                </div>
                <span className="badge badge-gray">{count}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default Dashboard;
