/**
 * Header Component
 * 
 * Top header bar with system status and user info
 */

import { useEffect, useState } from 'react';
import { CheckCircle2, XCircle, AlertCircle, Loader2 } from 'lucide-react';
import { healthService } from '@/services';
import type { HealthResponse } from '@/types';

const Header: React.FC = () => {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    checkHealth();
    // Check health every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const checkHealth = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const response = await healthService.checkHealth();
      setHealth(response);
    } catch (err) {
      setError('Unable to connect to API');
      setHealth(null);
    } finally {
      setIsLoading(false);
    }
  };

  const getStatusIcon = () => {
    if (isLoading) {
      return <Loader2 className="w-4 h-4 text-gray-400 animate-spin" />;
    }
    if (error || !health) {
      return <XCircle className="w-4 h-4 text-red-500" />;
    }
    if (health.status === 'healthy') {
      return <CheckCircle2 className="w-4 h-4 text-green-500" />;
    }
    return <AlertCircle className="w-4 h-4 text-yellow-500" />;
  };

  const getStatusText = () => {
    if (isLoading) return 'Checking...';
    if (error) return error;
    if (!health) return 'Offline';
    return health.status === 'healthy' ? 'Online' : 'Degraded';
  };

  const getStatusColor = () => {
    if (isLoading || !health) return 'text-gray-600';
    if (error) return 'text-red-600';
    if (health.status === 'healthy') return 'text-green-600';
    return 'text-yellow-600';
  };

  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-20">
      <div className="px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          {/* Page Title - will be updated by individual pages */}
          <div>
            <h2 className="text-2xl font-semibold text-gray-900">
              Welcome to RAG System
            </h2>
            <p className="text-sm text-gray-500 mt-1">
              Intelligent document search and Q&A
            </p>
          </div>

          {/* Status Indicators */}
          <div className="flex items-center space-x-6">
            {/* API Status */}
            <div className="flex items-center space-x-2">
              {getStatusIcon()}
              <div className="text-sm">
                <p className="text-gray-500">API Status</p>
                <p className={cn('font-medium', getStatusColor())}>{getStatusText()}</p>
              </div>
            </div>

            {/* OpenAI Status */}
            {health && (
              <div className="flex items-center space-x-2">
                {health.openai_configured ? (
                  <CheckCircle2 className="w-4 h-4 text-green-500" />
                ) : (
                  <XCircle className="w-4 h-4 text-red-500" />
                )}
                <div className="text-sm">
                  <p className="text-gray-500">OpenAI</p>
                  <p
                    className={cn(
                      'font-medium',
                      health.openai_configured ? 'text-green-600' : 'text-red-600'
                    )}
                  >
                    {health.openai_configured ? 'Configured' : 'Not configured'}
                  </p>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

function cn(...classes: string[]) {
  return classes.filter(Boolean).join(' ');
}

export default Header;
