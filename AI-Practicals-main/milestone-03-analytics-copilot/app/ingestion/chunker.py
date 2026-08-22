"""
Chunk documents using LangChain.
"""

from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(documents):
    """
    Split documents into chunks.
    """

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = splitter.split_documents(documents)

    for chunk in chunks:
        source = chunk.metadata.get("source")
        if source:
            chunk.metadata["source"] = Path(str(source)).name
        else:
            chunk.metadata["source"] = "sample.pdf"

    return chunks
