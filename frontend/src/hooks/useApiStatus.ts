import { useEffect, useState } from 'react';

interface UseApiStatusReturn {
  isConnected: boolean;
  isLoading: boolean;
  error: string | null;
}

export const useApiStatus = (dependencies: React.DependencyList = []): UseApiStatusReturn => {
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const checkConnection = async () => {
      try {
        setIsLoading(true);
        const response = await fetch('http://127.0.0.1:8000/health');
        setIsConnected(response.ok);
        setError(null);
      } catch (err) {
        setIsConnected(false);
        setError('Cannot connect to backend API');
      } finally {
        setIsLoading(false);
      }
    };

    checkConnection();
  }, dependencies);

  return { isConnected, isLoading, error };
};
