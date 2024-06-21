import os
from utils.error_handling import log_error


def safe_delete(file_path: str) -> None:
    try:
        os.remove(file_path)
    except Exception as e:
        log_error(f"Error deleting temporary file {file_path}: {str(e)}")
