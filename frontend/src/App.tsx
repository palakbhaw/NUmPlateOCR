import { useState } from 'react';
import { ImageUpload } from './components/ImageUpload';
import { ImagePreview } from './components/ImagePreview';
import { ResultDisplay } from './components/ResultDisplay';
import { ConnectionStatus } from './components/ConnectionStatus';
import { useImageUpload } from './hooks/useImageUpload';
import { useApiStatus } from './hooks/useApiStatus';
import { ocrService } from './services/ocrService';

function App() {
  const { preview, file, handleFileChange, clearImage } = useImageUpload();
  const { isConnected, isLoading: statusLoading, error: statusError } = useApiStatus();
  
  const [result, setResult] = useState<string>('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingError, setProcessingError] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleDragEnter = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files?.length > 0) {
      const file = files[0];
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onloadend = () => {
          const event = {
            target: {
              files: [file],
            },
          } as unknown as React.ChangeEvent<HTMLInputElement>;
          handleFileChange(event);
        };
        reader.readAsDataURL(file);
      }
    }
  };

  const handleUpload = async () => {
    if (!file || !isConnected) {
      setProcessingError('Please select an image and ensure the backend is connected');
      return;
    }

    setIsProcessing(true);
    setProcessingError(null);
    setResult('');

    try {
      const response = await ocrService.uploadImage(file);
      if (response.result) {
        setResult(response.result);
      } else if (response.error) {
        setProcessingError(response.error);
      } else {
        setResult(JSON.stringify(response));
      }
    } catch (error) {
      setProcessingError(
        error instanceof Error ? error.message : 'Failed to process image'
      );
    } finally {
      setIsProcessing(false);
    }
  };

  const handleClear = () => {
    clearImage();
    setResult('');
    setProcessingError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center gap-3">
            <div className="bg-primary-600 text-white rounded-lg p-2">
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </div>
            <div>
              <h1 className="text-2xl font-bold text-gray-900">NumPlate OCR</h1>
              <p className="text-sm text-gray-600">License Plate Recognition powered by AI</p>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Connection Status */}
        <div className="mb-6">
          <ConnectionStatus
            isConnected={isConnected}
            isLoading={statusLoading}
            error={statusError}
          />
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Upload Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Upload Image</h2>
            
            {!preview ? (
              <div className="space-y-4">
                <ImageUpload
                  onFileSelect={handleFileChange}
                  isDragging={isDragging}
                  onDragEnter={handleDragEnter}
                  onDragLeave={handleDragLeave}
                  onDrop={handleDrop}
                />
                <p className="text-xs text-gray-500 text-center">
                  Supports: JPG, PNG, GIF (Max 10MB)
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <ImagePreview src={preview} onClear={handleClear} />
                <button
                  onClick={handleUpload}
                  disabled={!isConnected || isProcessing}
                  className={`w-full py-3 px-4 rounded-lg font-semibold transition-all ${
                    isConnected && !isProcessing
                      ? 'bg-primary-600 hover:bg-primary-700 text-white cursor-pointer'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  {isProcessing ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                      </svg>
                      Processing...
                    </span>
                  ) : (
                    'Extract License Plate'
                  )}
                </button>
              </div>
            )}
          </div>

          {/* Results Section */}
          <div className="bg-white rounded-lg shadow-lg p-6">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Recognition Result</h2>
            
            {result || processingError || isProcessing ? (
              <div className="space-y-4">
                <ResultDisplay
                  result={result}
                  isLoading={isProcessing}
                  error={processingError}
                />
                {result && (
                  <div className="flex gap-2">
                    <button
                      onClick={handleClear}
                      className="flex-1 py-2 px-4 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded-lg font-medium transition-colors"
                    >
                      New Upload
                    </button>
                    <button
                      onClick={() => {
                        navigator.clipboard.writeText(result);
                      }}
                      className="flex-1 py-2 px-4 bg-primary-600 hover:bg-primary-700 text-white rounded-lg font-medium transition-colors"
                    >
                      Copy
                    </button>
                  </div>
                )}
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-48 text-center">
                <svg className="w-16 h-16 text-gray-300 mb-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <p className="text-gray-500 font-medium">Upload an image to get started</p>
                <p className="text-sm text-gray-400 mt-1">Results will appear here</p>
              </div>
            )}
          </div>
        </div>

        {/* Info Section */}
        <div className="mt-8 bg-white rounded-lg shadow-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-3">How it works</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <p className="font-medium text-gray-900">Upload Image</p>
                <p className="text-gray-600 mt-1">Select or drag an image containing a license plate</p>
              </div>
            </div>
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <p className="font-medium text-gray-900">AI Processing</p>
                <p className="text-gray-600 mt-1">Advanced AI analyzes the image using GPT-4 Vision</p>
              </div>
            </div>
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-primary-100 text-primary-700 rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <p className="font-medium text-gray-900">Get Result</p>
                <p className="text-gray-600 mt-1">View and copy the extracted plate number instantly</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-gray-300 mt-16">
        <div className="max-w-4xl mx-auto px-4 py-8 text-center text-sm">
          <p>© 2026 NumPlate OCR. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}

export default App;
