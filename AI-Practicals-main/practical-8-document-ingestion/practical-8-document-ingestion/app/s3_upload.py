from pathlib import Path

import boto3

from app.config import settings


def upload_pdfs() -> None:
    """Upload PDFs from local folder to S3."""

    s3_client = boto3.client(
        "s3",
        region_name=settings.aws_region
    )

    pdf_directory = Path("data/pdfs")

    for pdf_file in pdf_directory.glob("*.pdf"):
        print(f"Uploading: {pdf_file.name}")

        s3_client.upload_file(
            str(pdf_file),
            settings.bucket_name,
            pdf_file.name
        )

    print("PDF upload completed.")