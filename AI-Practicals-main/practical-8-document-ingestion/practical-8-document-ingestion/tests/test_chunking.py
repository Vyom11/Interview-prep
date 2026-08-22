from app.chunking import chunk_document


def test_chunking() -> None:
    text = "Hello world " * 500

    chunks = chunk_document(
        text=text,
        chunk_size=200
    )

    assert len(chunks) > 1