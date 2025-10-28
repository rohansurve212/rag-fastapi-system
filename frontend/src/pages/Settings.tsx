/**
 * Settings Page
 * 
 * Placeholder for Phase 6 - Application settings
 */

import { Settings as SettingsIcon } from 'lucide-react';

const Settings: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Settings</h1>
        <p className="mt-1 text-sm text-gray-600">
          Configure your application preferences
        </p>
      </div>

      <div className="card text-center py-12">
        <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
          <SettingsIcon className="w-8 h-8 text-gray-600" />
        </div>
        <h3 className="text-lg font-medium text-gray-900 mb-2">
          Settings Coming Soon
        </h3>
        <p className="text-gray-600 mb-4">
          This feature will be available in Phase 6
        </p>
        <div className="inline-flex items-center space-x-2 text-sm text-gray-500">
          <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse" />
          <span>Phase 6: In Development</span>
        </div>
      </div>
    </div>
  );
};

export default Settings;
