import pytest
import os
from utils.environment import load_environment, get_env_variable


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest file
    after command line options have been parsed.
    """
    os.environ["PYTEST_CURRENT_TEST"] = "True"  # Force test environment
    load_environment()


@pytest.fixture(scope="session")
def access_token():
    return get_env_variable("ACCESS_TOKEN")


@pytest.fixture(scope="session")
def redis_url():
    return get_env_variable("REDIS_URL")


@pytest.fixture(scope="session")
def cache_expiration_seconds():
    return int(get_env_variable("CACHE_EXPIRATION_IN_SECONDS", "3600"))
