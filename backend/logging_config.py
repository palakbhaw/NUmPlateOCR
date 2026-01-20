import logging
import os
import sys

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

def setup_logger():
        logger = logging.getLogger()
        logger.setLevel(LOG_LEVEL)

        handler = logging.StreamHandler(sys.stdout)

        formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.handlers = [handler]

        logging.getLogger("uvicorn.access").setLevel(LOG_LEVEL)
        logging.getLogger("uvicorn.error").setLevel(LOG_LEVEL)

        return logger

