import { useState } from 'react';

interface UseImageUploadReturn {
  preview: string | null;
  file: File | null;
  handleFileChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  clearImage: () => void;
  setFile: (file: File | null) => void;
  setPreview: (preview: string | null) => void;
}

export const useImageUpload = (): UseImageUploadReturn => {
  const [preview, setPreview] = useState<string | null>(null);
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = event.target.files?.[0];
    if (selectedFile) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setPreview(reader.result as string);
        setFile(selectedFile);
      };
      reader.readAsDataURL(selectedFile);
    }
  };

  const clearImage = () => {
    setPreview(null);
    setFile(null);
  };

  return {
    preview,
    file,
    handleFileChange,
    clearImage,
    setFile,
    setPreview,
  };
};
