"""
Chunk documents using LangChain.
"""

# Import splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    """
    Split documents into chunks.
    """

    # Create splitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    # Split documents
    chunks = splitter.split_documents(documents)

    # Add metadata
    for chunk in chunks:

        chunk.metadata["source"] = "sample.pdf"

    return chunks
