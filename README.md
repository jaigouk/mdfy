# mdfy

mdfy is a FastAPI-based web service that converts various document formats to Markdown.

This repository contains the source code for the PDF to Markdown conversion service, which uses code from the [RAG project](https://github.com/pymupdf/RAG/tree/main).

## Features

- Convert PDF, DOCX, XLSX, PPTX, HWP, OXPS, EPUB, and MOBI files to Markdown
- Process files from URLs or direct uploads
- Redis caching for improved performance
- OAuth2 authentication for secure access

## Prerequisites

- Python 3.11+
- Poetry
- Redis server
- Docker (optional)

## Installation

1. Clone the repository:

```sh
git clone https://github.com/jaigouk/mdfy.git
cd mdfy
```

2. Create a virtual environment and activate it:

```sh
conda create -n mdfy python=3.11
conda activate mdfy
```

3. Install the required packages:
```sh
poetry install
```

4. Copy the `.env.example` file to `.env` and fill in the required values:
```sh
cp .env.example .env
```

## Running the server

### Local development
```sh
poetry run uvicorn mdfy:app --reload
```
The server will be available at `http://127.0.0.1:8000`.

### Production (using Docker)

1. Build the Docker image:
```sh
docker build -t mdfy .
```

2. Run the container:
```sh
docker run -p 8000:8000 --env-file .env mdfy
```

The server will be available at `http://localhost:8000`.

## API Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint
- `POST /process_url/`: Convert a document from a URL to Markdown
- `POST /process_upload/`: Convert an uploaded document to Markdown

FastAPI automatically generates interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

You can use these interfaces to explore and test the API endpoints.


## OpenAPI Specification

The OpenAPI (Swagger) specification is available at:
http://127.0.0.1:8000/openapi.json

## Running Tests

```
poetry run pytest
```

## License

This project is licensed under the GNU AGPL v3.0 License - see the [LICENSE](LICENSE) file for details.
