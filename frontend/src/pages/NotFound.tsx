/**
 * NotFound Page
 * 
 * 404 error page for invalid routes
 */

import { Link } from 'react-router-dom';
import { Home, ArrowLeft } from 'lucide-react';

const NotFound: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="max-w-md w-full text-center">
        {/* 404 Illustration */}
        <div className="mb-8">
          <h1 className="text-9xl font-bold text-primary-600">404</h1>
          <div className="mt-4">
            <div className="inline-block p-4 bg-primary-100 rounded-full">
              <svg
                className="w-16 h-16 text-primary-600"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
          </div>
        </div>

        {/* Error Message */}
        <h2 className="text-3xl font-bold text-gray-900 mb-2">Page Not Found</h2>
        <p className="text-lg text-gray-600 mb-8">
          Sorry, we couldn't find the page you're looking for. It might have been moved or
          deleted.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link
            to="/"
            className="inline-flex items-center justify-center px-6 py-3 btn btn-primary"
          >
            <Home className="w-5 h-5 mr-2" />
            Back to Home
          </Link>
          <button
            onClick={() => window.history.back()}
            className="inline-flex items-center justify-center px-6 py-3 btn btn-secondary"
          >
            <ArrowLeft className="w-5 h-5 mr-2" />
            Go Back
          </button>
        </div>

        {/* Help Text */}
        <div className="mt-12 pt-8 border-t border-gray-200">
          <p className="text-sm text-gray-500">
            Need help?{' '}
            <Link to="/" className="text-primary-600 hover:text-primary-700 font-medium">
              Contact support
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default NotFound;
