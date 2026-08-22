from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_document(
    text: str,
    chunk_size: int
) -> list[str]:
    """Split text into chunks."""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=int(chunk_size * 0.1)
    )

    return splitter.split_text(text)