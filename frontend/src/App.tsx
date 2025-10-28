/**
 * App Component
 * 
 * Main application component with routing and error boundary
 */

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, ErrorBoundary } from '@/components';
import {
  Dashboard,
  Documents,
  SearchPage,
  ChatPage,
  Health,
  Settings,
  NotFound,
} from '@/pages';
import './index.css';

function App() {
  return (
    <ErrorBoundary>
      <Router>
        <Routes>
          {/* Main Layout Routes */}
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="documents" element={<Documents />} />
            <Route path="search" element={<SearchPage />} />
            <Route path="chat" element={<ChatPage />} />
            <Route path="health" element={<Health />} />
            <Route path="settings" element={<Settings />} />
          </Route>

          {/* 404 - Not Found */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </ErrorBoundary>
  );
}

export default App;
