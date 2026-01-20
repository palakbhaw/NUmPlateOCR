import React from 'react';

interface ConnectionStatusProps {
  isConnected: boolean;
  isLoading: boolean;
  error?: string | null;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({
  isConnected,
  isLoading,
  error,
}) => {
  if (isLoading) {
    return (
      <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3 flex items-center gap-2">
        <div className="animate-spin">
          <svg className="w-4 h-4 text-yellow-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </div>
        <p className="text-sm text-yellow-700">Checking connection...</p>
      </div>
    );
  }

  if (isConnected) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-3 flex items-center gap-2">
        <div className="w-2 h-2 bg-green-600 rounded-full"></div>
        <p className="text-sm text-green-700 font-medium">Backend API connected</p>
      </div>
    );
  }

  return (
    <div className="bg-red-50 border border-red-200 rounded-lg p-3">
      <p className="text-sm text-red-700 font-medium">⚠️ Backend not available</p>
      <p className="text-xs text-red-600 mt-1">{error || 'Make sure the backend server is running on http://127.0.0.1:8000'}</p>
    </div>
  );
};
