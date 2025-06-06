import re
import tempfile
import os
import time
import zipfile
import io
from docling.document_converter import DocumentConverter

def split_document_into_sections(markdown_text):
    sections = re.split(r'(?=^##\s)', markdown_text, flags=re.MULTILINE)
    section_dict = {}

    for section in sections:
        if section.strip():
            title_match = re.match(r'^##\s*(.*?)(?:\n|$)', section)
            if title_match:
                title = title_match.group(1).strip()
                clean_title = re.sub(r'[^\w\s-]', '', title).strip().replace(' ', '_')
                section_dict[clean_title] = section.strip()

    return section_dict

def convert_pdf_to_zip(source_path_or_url: str, is_url: bool = False) -> bytes:
    converter = DocumentConverter()

    if is_url:
        result = converter.convert(source_path_or_url)
    else:
        result = converter.convert(source_path_or_url)

    markdown_text = result.document.export_to_markdown()
    sections = split_document_into_sections(markdown_text)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for section_name, section_content in sections.items():
            zip_file.writestr(f"{section_name}.md", section_content)

    zip_buffer.seek(0)
    return zip_buffer.getvalue()
