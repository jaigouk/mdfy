import pytest
from fastapi import HTTPException
from converters.markdown_splitter import process_file, MarkdownToJson, convert_file_to_markdown
from unittest.mock import patch
import json
from returns.result import Success

# Sample markdown text for testing
SAMPLE_MARKDOWN = """# Title 1

Content 1

## Subtitle 1

Content 2

# Title 2

Content 3"""

EXPECTED_JSON = json.dumps(
    [
        {"title": "Title 1", "content": "Content 1\n\n## Subtitle 1\n\nContent 2"},
        {"title": "Title 2", "content": "Content 3"},
    ],
    indent=2,
)


@pytest.fixture
def sample_file_content():
    return b"Sample file content"


def test_markdown_to_json():
    converter = MarkdownToJson(SAMPLE_MARKDOWN)
    result = converter.call()
    assert result.unwrap() == [
        {"title": "Title 1", "content": "Content 1\n\n## Subtitle 1\n\nContent 2"},
        {"title": "Title 2", "content": "Content 3"},
    ]


def test_markdown_to_json_empty():
    converter = MarkdownToJson("")
    result = converter.call()
    assert result.unwrap() == []


# Update other tests as needed


@patch("converters.file_to_md.magic.from_buffer")
@patch("converters.file_to_md.convert_file_to_markdown")
@patch("converters.file_to_md.MarkdownToJson")
def test_process_file_success(
    mock_markdown_to_json, mock_convert, mock_magic, sample_file_content
):
    mock_magic.return_value = "application/pdf"
    mock_convert.return_value = SAMPLE_MARKDOWN
    mock_markdown_to_json.return_value.call.return_value = Success(EXPECTED_JSON)

    result = process_file(sample_file_content)

    assert json.loads(result) == json.loads(EXPECTED_JSON)
    mock_convert.assert_called_once()
    mock_markdown_to_json.assert_called_once_with(SAMPLE_MARKDOWN)


@patch("converters.file_to_md.magic.from_buffer")
def test_process_file_unsupported_format(mock_magic, sample_file_content):
    mock_magic.return_value = "application/unsupported"

    with pytest.raises(HTTPException) as excinfo:
        process_file(sample_file_content)

    assert excinfo.value.status_code == 415
    assert "Unsupported file format" in str(excinfo.value.detail)


@patch("converters.file_to_md.magic.from_buffer")
@patch("converters.file_to_md.convert_file_to_markdown")
def test_process_file_conversion_error(mock_convert, mock_magic, sample_file_content):
    mock_magic.return_value = "application/pdf"
    mock_convert.side_effect = Exception("Conversion error")

    with pytest.raises(HTTPException) as excinfo:
        process_file(sample_file_content)

    assert excinfo.value.status_code == 500
    assert "Error processing file" in str(excinfo.value.detail)


@patch("pymupdf4llm.to_markdown")
def test_convert_file_to_markdown(mock_to_markdown):
    mock_to_markdown.return_value = SAMPLE_MARKDOWN
    result = convert_file_to_markdown("test.pdf")
    assert result == SAMPLE_MARKDOWN
    mock_to_markdown.assert_called_once_with("test.pdf")
