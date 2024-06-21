import os


def test_env_variables(access_token, redis_url, cache_expiration_seconds):
    print("Current environment variables:")
    for key, value in os.environ.items():
        print(f"{key}: {value}")

    assert access_token == "test_access_token"
    assert redis_url == "redis://localhost:6379"
    assert cache_expiration_seconds == 60
