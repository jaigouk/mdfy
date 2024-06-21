import logging
from fastapi import HTTPException

logging.basicConfig(level=logging.ERROR, format="%(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def log_error(error: Exception) -> None:
    error_type = type(error).__name__
    logger.error(f"An error occurred: {error_type} - {str(error)}", exc_info=True)


def handle_error(error: Exception) -> HTTPException:
    log_error(error)
    return HTTPException(status_code=500, detail="An internal error occurred")
