import axios, { AxiosError } from 'axios';

const API_BASE_URL = ((import.meta as any).env.VITE_API_URL as string) || 'http://192.168.x.x:8000';

export interface OCRResponse {
  result?: string;
  error?: string;
}

export const ocrService = {
  uploadImage: async (file: File): Promise<OCRResponse> => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post<OCRResponse>(
        `${API_BASE_URL}/upload`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        }
      );

      return response.data;
    } catch (error) {
      const axiosError = error as AxiosError;
      throw new Error(
        axiosError.response?.data ? JSON.stringify(axiosError.response.data) : 'Failed to process image'
      );
    }
  },

  healthCheck: async (): Promise<boolean> => {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return response.status === 200;
    } catch {
      return false;
    }
  },
};
