import pytest
from converters.markdown_splitter import MarkdownSplitter
from unittest.mock import patch
from returns.result import Success, Failure

SAMPLE_MARKDOWN = """# Title 1

Content 1

## Subtitle 1

Content 2

# Title 2

Content 3"""

EXPECTED_SECTIONS = [
    {"title": "Title 1", "content": "Content 1\n\n## Subtitle 1\n\nContent 2"},
    {"title": "Title 2", "content": "Content 3"},
]


@pytest.fixture
def sample_file_content():
    return b"Sample file content"


def test_markdown_splitter_success():
    with patch(
        "converters.markdown_splitter.magic.from_buffer", return_value="application/pdf"
    ), patch(
        "converters.markdown_splitter.pymupdf4llm.to_markdown",
        return_value=SAMPLE_MARKDOWN,
    ):
        splitter = MarkdownSplitter()
        result = splitter.call(b"dummy content")
        assert isinstance(result, Success)
        assert result.unwrap() == EXPECTED_SECTIONS


def test_markdown_splitter_empty():
    with patch(
        "converters.markdown_splitter.magic.from_buffer", return_value="application/pdf"
    ), patch("converters.markdown_splitter.pymupdf4llm.to_markdown", return_value=""):
        splitter = MarkdownSplitter()
        result = splitter.call(b"dummy content")
        assert isinstance(result, Success)
        assert result.unwrap() == []


def test_markdown_splitter_unsupported_format():
    with patch(
        "converters.markdown_splitter.magic.from_buffer",
        return_value="application/unsupported",
    ):
        splitter = MarkdownSplitter()
        result = splitter.call(b"dummy content")
        assert isinstance(result, Failure)
        assert "Unsupported file format" in str(result.failure())


def test_markdown_splitter_conversion_error():
    with patch(
        "converters.markdown_splitter.magic.from_buffer", return_value="application/pdf"
    ), patch(
        "converters.markdown_splitter.pymupdf4llm.to_markdown",
        side_effect=Exception("Conversion error"),
    ):
        splitter = MarkdownSplitter()
        result = splitter.call(b"dummy content")
        assert isinstance(result, Failure)
        assert "Conversion error" in str(result.failure())
