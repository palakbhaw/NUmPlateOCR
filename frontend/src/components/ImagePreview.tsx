import React from 'react';

interface ImagePreviewProps {
  src: string;
  alt?: string;
  onClear?: () => void;
}

export const ImagePreview: React.FC<ImagePreviewProps> = ({
  src,
  alt = 'Preview',
  onClear,
}) => {
  return (
    <div className="relative bg-gray-100 rounded-lg overflow-hidden">
      <img
        src={src}
        alt={alt}
        className="w-full h-auto max-h-96 object-cover"
      />
      {onClear && (
        <button
          onClick={onClear}
          className="absolute top-3 right-3 bg-red-500 hover:bg-red-600 text-white rounded-full p-2 transition-colors"
          title="Remove image"
        >
          <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      )}
    </div>
  );
};
