import os
from dotenv import load_dotenv


def load_environment():
    """Load the appropriate environment file based on the current context."""
    if "PYTEST_CURRENT_TEST" in os.environ:
        # We're in a test environment
        env_file = ".env.test"
    elif os.environ.get("ENVIRONMENT") == "production":
        # We're in production
        env_file = ".env.production"
    else:
        # Default to development
        env_file = ".env"

    env_path = os.path.join(os.getcwd(), env_file)
    if os.path.exists(env_path):
        load_dotenv(env_path)
        print(f"Loaded environment from {env_path}")
    else:
        print(f"Warning: {env_path} does not exist")

    print(f"Current working directory: {os.getcwd()}")
    print("Environment variables after loading:")
    for key in ["ACCESS_TOKEN", "REDIS_URL", "CACHE_EXPIRATION_IN_SECONDS"]:
        print(f"{key}: {os.getenv(key)}")


def get_env_variable(key: str, default: str = None) -> str:
    """
    Get an environment variable, raising an error if it's not found and no default is provided.
    """
    value = os.getenv(key, default)
    if value is None:
        raise ValueError(
            f"Environment variable {key} is not set and no default value was provided."
        )
    return value
