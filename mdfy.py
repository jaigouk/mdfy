from fastapi import Depends, FastAPI, HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import PlainTextResponse
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from fastapi_cache.backends.redis import RedisBackend
from starlette.responses import Response
import requests
from converters.markdown_splitter import MarkdownSplitter
from utils.error_handling import handle_error
from utils.environment import load_environment, get_env_variable
from returns.pipeline import is_successful

load_environment()

ACCESS_TOKEN = get_env_variable("ACCESS_TOKEN")
REDIS_URL: str = get_env_variable("REDIS_URL")
CACHE_EXPIRATION_IN_SECONDS = int(
    get_env_variable("CACHE_EXPIRATION_IN_SECONDS", "3600")
)

app = FastAPI(
    title="mdfy",
    description="A service to convert various file formats to Markdown",
    version="0.1.0",
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.on_event("startup")
async def startup():
    redis = RedisBackend(REDIS_URL)
    FastAPICache.init(redis, prefix="fastapi-cache")


@app.get("/", response_class=PlainTextResponse)
async def root():
    return "Welcome to mdfy - a service to convert various file formats to Markdown"


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/process_url/")
@cache(expire=CACHE_EXPIRATION_IN_SECONDS)
async def process_url(
    url: str, token: str = Depends(oauth2_scheme), response: Response = None
):
    if token != ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    try:
        response = requests.get(url)
        response.raise_for_status()
        splitter = MarkdownSplitter()
        result = splitter.call(response.content)
        if is_successful(result):
            response.headers["X-Cached"] = "true"
            return {"sections": result.unwrap()}
        else:
            raise HTTPException(status_code=500, detail="Failed to process file")
    except requests.RequestException as e:
        raise HTTPException(
            status_code=422, detail=f"Could not process the file from URL: {str(e)}"
        )
    except Exception as e:
        return handle_error(e)


@app.post("/process_upload/")
async def process_upload(
    file: UploadFile = File(...), token: str = Depends(oauth2_scheme)
):
    if token != ACCESS_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid access token"
        )

    try:
        file_content = await file.read()
        splitter = MarkdownSplitter()
        result = splitter.call(file_content)
        if is_successful(result):
            return {"sections": result.unwrap()}
        else:
            raise HTTPException(status_code=500, detail="Failed to process file")
    except Exception as e:
        return handle_error(e)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
