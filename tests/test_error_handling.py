from fastapi import HTTPException
from utils.error_handling import handle_error, log_error


def test_handle_error():
    error = ValueError("Test error")
    result = handle_error(error)

    assert isinstance(result, HTTPException)
    assert result.status_code == 500
    assert result.detail == "An internal error occurred"


def test_log_error(caplog):
    error = ValueError("Test error")
    log_error(error)

    assert "An error occurred: ValueError - Test error" in caplog.text


def test_handle_error_logs_error(caplog):
    error = ValueError("Test error")
    handle_error(error)

    assert "An error occurred: ValueError - Test error" in caplog.text
