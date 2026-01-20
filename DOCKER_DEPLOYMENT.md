# NumPlateOCR - Docker Deployment Guide

## Prerequisites
- Docker installed ([Download Docker](https://www.docker.com/products/docker-desktop))
- Docker Compose installed (comes with Docker Desktop)

## Deployment Steps

### 1. Build and Run with Docker Compose

```bash
# Navigate to the project root directory
cd NumPlateOCR

# Build images and start containers
docker-compose up --build
```

### 2. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 3. Environment Variables

Make sure your `.env` file exists in the `backend/` directory with necessary configurations (e.g., API keys).

```bash
```

## Docker Commands

### Start containers
```bash
docker-compose up
```

### Stop containers
```bash
docker-compose down
```

### View logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Rebuild images
```bash
docker-compose build --no-cache
```

### Remove containers and volumes
```bash
docker-compose down -v
```

## Production Deployment

For production, consider:

1. **Update docker-compose.yml** for production URLs and remove volume mounts
2. **Use environment-specific files**: 
   - `docker-compose.prod.yml` for production
   - `docker-compose.dev.yml` for development

3. **Security**: 
   - Don't commit `.env` files
   - Use Docker secrets or environment variables
   - Remove CORS debug origins

4. **Scaling**: Use Kubernetes or container orchestration services

## Troubleshooting

### Port already in use
```bash
# Change ports in docker-compose.yml or kill the process
lsof -i :8000  # Check what's using port 8000
```

### Container won't start
```bash
docker-compose logs backend
docker-compose logs frontend
```

### Rebuild specific service
```bash
docker-compose up --build backend
```

## File Structure

```
NumPlateOCR/
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── .env
│   └── ...
├── frontend/
│   ├── Dockerfile
│   ├── package.json
│   └── ...
├── docker-compose.yml
└── .dockerignore
```
