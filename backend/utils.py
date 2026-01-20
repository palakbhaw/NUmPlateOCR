import base64
import logging

logger = logging.getLogger(__name__)


def img_to_base64(img_bytes: bytes)-> str:
    logger.debug("Converting image bytes to base64")
    return base64.b64encode(img_bytes).decode('utf-8')

