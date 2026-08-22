"""
Download documents from S3.
"""

# Import S3 client
from app.core.aws_clients import s3_client

# Import config
from app.core.config import S3_BUCKET_NAME


def download_file_from_s3(s3_key: str, local_path: str) -> str:
    """
    Download PDF from S3 bucket.
    """

    # Download file
    s3_client.download_file(S3_BUCKET_NAME, s3_key, local_path)

    return local_path
