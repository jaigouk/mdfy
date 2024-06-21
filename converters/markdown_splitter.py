import tempfile
import magic
from utils.file_operations import safe_delete
from utils.error_handling import log_error
import re
from typing import List
from returns.result import Result, Success, Failure
from typing_extensions import TypedDict
import pymupdf4llm


class Section(TypedDict):
    title: str
    content: str


class MarkdownSplitter:
    ALLOWED_FILE_TYPES = [
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/vnd.ms-powerpoint",
        "application/x-hwp",
        "application/oxps",
        "application/epub+zip",
        "application/x-mobipocket-ebook",
    ]

    def call(self, file_content: bytes) -> Result[List[Section], Exception]:
        try:
            md_text = self._process_file(file_content)
            sections = self._split_markdown(md_text)
            return Success(sections)
        except Exception as e:
            log_error(e)
            return Failure(e)

    def _process_file(self, file_content: bytes) -> str:
        mime = magic.from_buffer(file_content, mime=True)
        if mime not in self.ALLOWED_FILE_TYPES:
            raise ValueError(f"Unsupported file format: {mime}")

        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp.write(file_content)
            temp_path = temp.name

        try:
            return self._convert_file_to_markdown(temp_path)
        finally:
            safe_delete(temp_path)

    def _convert_file_to_markdown(self, file_path: str) -> str:
        return pymupdf4llm.to_markdown(file_path)

    def _split_markdown(self, markdown_text: str) -> List[Section]:
        markdown_text = markdown_text.strip()
        if not markdown_text:
            return []

        lines = markdown_text.split("\n")
        sections = []
        current_section = None
        current_content = []

        for line in lines:
            title_match = re.match(r"^(#+)\s*(.*)", line)
            if title_match:
                level = len(title_match.group(1))
                title = title_match.group(2).strip()
                if level == 1:
                    if current_section:
                        current_section["content"] = "\n".join(current_content).strip()
                        sections.append(current_section)
                    current_section = Section(title=title, content="")
                    current_content = []
                else:
                    current_content.append(line)
            else:
                current_content.append(line)

        if current_section:
            current_section["content"] = "\n".join(current_content).strip()
            sections.append(current_section)

        return sections
