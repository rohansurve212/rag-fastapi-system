/**
 * Layout Component
 * 
 * Main application layout with sidebar and content area
 */

import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

interface LayoutProps {
  children?: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="lg:pl-64">
        {/* Header */}
        <Header />

        {/* Page Content */}
        <main className="py-6 px-4 sm:px-6 lg:px-8">
          <div className="mx-auto max-w-7xl">
            {children || <Outlet />}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;
