"""
Extract text using PyPDFLoader.
"""

# Import PyPDFLoader
from langchain_community.document_loaders import PyPDFLoader


def extract_pdf_documents(file_path: str):
    """
    Extract PDF documents.
    """

    # Create loader
    loader = PyPDFLoader(file_path)

    # Load documents
    documents = loader.load()

    return documents
