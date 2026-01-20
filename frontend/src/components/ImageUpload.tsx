import React from 'react';

interface ImageUploadProps {
  onFileSelect: (event: React.ChangeEvent<HTMLInputElement>) => void;
  isDragging?: boolean;
  onDragEnter?: (event: React.DragEvent<HTMLDivElement>) => void;
  onDragLeave?: (event: React.DragEvent<HTMLDivElement>) => void;
  onDrop?: (event: React.DragEvent<HTMLDivElement>) => void;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({
  onFileSelect,
  isDragging = false,
  onDragEnter,
  onDragLeave,
  onDrop,
}) => {
  return (
    <div
      className={`relative w-full border-2 border-dashed rounded-lg p-8 text-center transition-all cursor-pointer ${
        isDragging
          ? 'border-primary-600 bg-primary-50'
          : 'border-gray-300 hover:border-primary-500 hover:bg-gray-50'
      }`}
      onDragEnter={onDragEnter}
      onDragLeave={onDragLeave}
      onDrop={onDrop}
    >
      <input
        type="file"
        accept="image/*"
        onChange={onFileSelect}
        className="hidden"
        id="image-input"
      />
      <label htmlFor="image-input" className="cursor-pointer block">
        <div className="flex flex-col items-center gap-3">
          <svg
            className="w-12 h-12 text-primary-600"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          <div>
            <p className="text-lg font-semibold text-gray-900">Click to upload or drag and drop</p>
            <p className="text-sm text-gray-500 mt-1">PNG, JPG, GIF up to 10MB</p>
          </div>
        </div>
      </label>
    </div>
  );
};
