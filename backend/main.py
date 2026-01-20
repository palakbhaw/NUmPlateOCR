import time
import uuid
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from llm import llm_processing
from logging_config import setup_logger
import logging 

logger = setup_logger()

app = FastAPI(title="License Plate API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("https")
async def log_requests(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"[{request_id}] {request.method} {request.url.path}")

    try:
        response = await call_next(request)
        duration = round(time.time() - start_time, 3)

        logger.info(
            f"[{request_id}] Completed in {duration}s | Status {response.status_code}"
        )

        response.headers["X-Request-ID"] = request_id
        return response

    except Exception:
        logger.exception(f"[{request_id}] Request failed")
        raise



@app.post('/upload')
async def upload_image(file: UploadFile = File(...)):
    logger.info(f"Received file: {file.filename}")

    image = await file.read()
    
    answer =  llm_processing(image)
    
    return answer

@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception("Unhandled exception occurred")
    return {
        "error": "Internal server error"
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")