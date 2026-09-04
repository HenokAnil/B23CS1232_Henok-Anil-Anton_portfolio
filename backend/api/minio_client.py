import os
import boto3
from botocore.client import Config
import logging

logger = logging.getLogger(__name__)

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin123")
DEFAULT_BUCKET = os.getenv("MINIO_BUCKET", "seismic-waveforms")

class MinIOStorage:
    def __init__(self, endpoint=MINIO_ENDPOINT, access_key=MINIO_ACCESS_KEY, secret_key=MINIO_SECRET_KEY, bucket=DEFAULT_BUCKET):
        self.endpoint = endpoint
        self.bucket = bucket
        self.s3 = boto3.client(
            "s3",
            endpoint_url=self.endpoint,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            config=Config(signature_version="s3v4"),
            region_name="us-east-1"
        )
        self.ensure_bucket()

    def ensure_bucket(self):
        try:
            buckets = [b["Name"] for b in self.s3.list_buckets().get("Buckets", [])]
            if self.bucket not in buckets:
                self.s3.create_bucket(Bucket=self.bucket)
                logger.info(f"Created MinIO bucket '{self.bucket}'")
            else:
                logger.info(f"MinIO bucket '{self.bucket}' ready")
        except Exception as e:
            logger.error(f"Error ensuring MinIO bucket '{self.bucket}': {e}")

    def upload_bytes(self, key: str, data: bytes, content_type: str = "application/octet-stream") -> str:
        self.s3.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType=content_type
        )
        return key

    def download_bytes(self, key: str) -> bytes:
        response = self.s3.get_object(Bucket=self.bucket, Key=key)
        return response["Body"].read()

# Singleton instance
minio_storage = MinIOStorage()
