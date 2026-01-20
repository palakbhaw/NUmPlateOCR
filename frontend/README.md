# NumPlate OCR Frontend

A modern, responsive React + Vite + TypeScript frontend for license plate recognition using AI.

## Features

- 🚀 **Fast & Modern**: Built with React, Vite, and TypeScript
- 🎨 **Beautiful UI**: Styled with Tailwind CSS
- 🖼️ **Image Upload**: Drag-and-drop and click-to-upload support
- ⚡ **Real-time Processing**: Instant license plate recognition
- 📱 **Responsive Design**: Works perfectly on desktop, tablet, and mobile
- 🔗 **API Integration**: Seamless connection with backend service
- ✨ **Copy Result**: One-click copy of recognized plate numbers

## Prerequisites

- Node.js 16+ and npm (or yarn)
- Backend API running on `http://127.0.0.1:8000`

## Installation

1. **Install dependencies**:
   ```bash
   npm install
   ```

2. **Create environment file** (optional):
   ```bash
   cp .env.example .env
   ```

## Development

Start the development server:

```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## Build

Create a production build:

```bash
npm run build
```

Preview the production build:

```bash
npm run preview
```

## Project Structure

```
frontend/
├── src/
│   ├── components/          # React components
│   │   ├── ImageUpload.tsx  # Image upload component
│   │   ├── ImagePreview.tsx # Image preview component
│   │   ├── ResultDisplay.tsx # Results display component
│   │   └── ConnectionStatus.tsx # Backend status indicator
│   ├── hooks/               # Custom React hooks
│   │   ├── useImageUpload.ts # Image upload logic
│   │   └── useApiStatus.ts  # API connection check
│   ├── services/            # API services
│   │   └── ocrService.ts    # OCR API client
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # Application entry point
│   └── index.css            # Global styles
├── index.html               # HTML template
├── package.json             # Dependencies
├── tailwind.config.js       # Tailwind CSS configuration
├── tsconfig.json            # TypeScript configuration
└── vite.config.ts           # Vite configuration
```

## Technologies

- **React 18**: UI framework
- **Vite**: Build tool
- **TypeScript**: Type safety
- **Tailwind CSS**: Styling
- **Axios**: HTTP client
- **PostCSS & Autoprefixer**: CSS processing

## API Integration

The frontend communicates with the backend API through the `ocrService`:

- **Base URL**: `http://127.0.0.1:8000`
- **Upload Endpoint**: `POST /upload` - Send image for license plate extraction
- **Health Check**: `GET /health` - Check backend connectivity

## Features

### Image Upload
- Click or drag-and-drop to upload images
- Supports JPG, PNG, and GIF formats
- Maximum file size: 10MB

### Real-time Processing
- Automatic image processing upon upload
- Real-time feedback with loading indicators
- Error handling and user-friendly messages

### Result Display
- Clear display of extracted license plate number
- One-click copy functionality
- Visual feedback for success and errors

### Connection Monitoring
- Real-time backend connectivity status
- Automatic connection checking on app load
- User-friendly connection status messages

## Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

MIT
