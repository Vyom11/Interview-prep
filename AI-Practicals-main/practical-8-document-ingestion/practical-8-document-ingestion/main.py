import argparse

from app.s3_upload import upload_pdfs
from app.textract_service import extract_documents
from app.indexing import run_indexing_pipeline


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--chunk-size", type=int, default=500)

    args = parser.parse_args()

    upload_pdfs()
    extract_documents()

    run_indexing_pipeline(chunk_size=args.chunk_size)


if __name__ == "__main__":
    main()