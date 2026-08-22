"""
Local PDF text extraction service.
"""

import json
from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader


def extract_text_from_pdf(pdf_path: Path) -> str:
    """
    Extract text from PDF using PyPDFLoader.
    """

    loader = PyPDFLoader(str(pdf_path))

    pages = loader.load()

    full_text = "\n".join(page.page_content for page in pages)

    return full_text


def extract_documents() -> None:
    """
    Extract text from all PDFs locally.
    """

    pdf_directory = Path("data/pdfs")

    extracted_directory = Path("data/extracted")

    for pdf_file in pdf_directory.glob("*.pdf"):

        print(f"Extracting: {pdf_file.name}")

        text = extract_text_from_pdf(pdf_file)

        output_path = extracted_directory / f"{pdf_file.stem}.json"

        with open(output_path, "w", encoding="utf-8") as file:

            json.dump({"text": text}, file, ensure_ascii=False, indent=2)

        print(f"Extracted: {pdf_file.name}")
