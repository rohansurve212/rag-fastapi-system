/**
 * Sidebar Component
 * 
 * Navigation sidebar with links to all main features
 */

import { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  Home,
  FileText,
  Search,
  MessageSquare,
  Settings,
  Activity,
  Menu,
  X,
} from 'lucide-react';
import { cn } from '@/utils';

interface NavItem {
  name: string;
  href: string;
  icon: React.ElementType;
}

const navigation: NavItem[] = [
  { name: 'Dashboard', href: '/', icon: Home },
  { name: 'Documents', href: '/documents', icon: FileText },
  { name: 'Search', href: '/search', icon: Search },
  { name: 'Chat', href: '/chat', icon: MessageSquare },
  { name: 'Health', href: '/health', icon: Activity },
  { name: 'Settings', href: '/settings', icon: Settings },
];

const Sidebar: React.FC = () => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <>
      {/* Mobile menu button */}
      <div className="lg:hidden fixed top-0 left-0 right-0 z-40 bg-white border-b border-gray-200">
        <div className="flex items-center justify-between px-4 py-3">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">RAG</span>
            </div>
            <span className="text-lg font-semibold text-gray-900">RAG System</span>
          </div>
          <button
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
            className="p-2 rounded-lg text-gray-600 hover:bg-gray-100"
          >
            {isMobileMenuOpen ? (
              <X className="w-6 h-6" />
            ) : (
              <Menu className="w-6 h-6" />
            )}
          </button>
        </div>
      </div>

      {/* Mobile menu overlay */}
      {isMobileMenuOpen && (
        <div
          className="lg:hidden fixed inset-0 z-30 bg-gray-900 bg-opacity-50"
          onClick={() => setIsMobileMenuOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside
        className={cn(
          'fixed top-0 left-0 z-40 h-screen w-64 bg-white border-r border-gray-200 transition-transform duration-300',
          'lg:translate-x-0',
          isMobileMenuOpen ? 'translate-x-0' : '-translate-x-full'
        )}
      >
        {/* Logo */}
        <div className="flex items-center space-x-2 px-6 py-4 border-b border-gray-200">
          <div className="w-10 h-10 bg-primary-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold">RAG</span>
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-900">RAG System</h1>
            <p className="text-xs text-gray-500">Document Q&A</p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          {navigation.map((item) => {
            const Icon = item.icon;
            const active = isActive(item.href);

            return (
              <Link
                key={item.name}
                to={item.href}
                onClick={() => setIsMobileMenuOpen(false)}
                className={cn(
                  'flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors',
                  active
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-700 hover:bg-gray-100'
                )}
              >
                <Icon className={cn('w-5 h-5', active ? 'text-primary-600' : 'text-gray-500')} />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        {/* Footer */}
        <div className="border-t border-gray-200 px-3 py-4">
          <div className="px-3 py-2">
            <p className="text-xs text-gray-500">Version 1.0.0</p>
            <p className="text-xs text-gray-400 mt-1">Phase 2 Complete ✓</p>
          </div>
        </div>
      </aside>

      {/* Spacer for mobile when menu is closed */}
      <div className="lg:hidden h-14" />
    </>
  );
};

export default Sidebar;
