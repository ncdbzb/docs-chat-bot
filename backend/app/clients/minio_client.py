from minio import Minio
from minio.error import S3Error
import io
import logging

from config import settings

class MinioClient:
    def __init__(self):
        self.client = Minio(
            settings.MINIO_ENDPOINT,
            access_key=settings.MINIO_ACCESS_KEY,
            secret_key=settings.MINIO_SECRET_KEY,
            secure=settings.MINIO_SECURE,
        )
        self.bucket_name = settings.MINIO_BUCKET_NAME
        self.root_path = settings.MINIO_ROOT_PATH.strip("/")

        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            logging.error(f"MinIO bucket error: {e}")
            raise

    def _get_object_name(self, filename: str) -> str:
        return f"{self.root_path}/{filename}" if self.root_path else filename

    def upload_document(self, file_bytes: bytes, object_name: str, content_type: str) -> None:
        object_name = self._get_object_name(object_name)
        try:
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=io.BytesIO(file_bytes),
                length=len(file_bytes),
                content_type=content_type
            )
        except S3Error as e:
            logging.error(f"Upload error for {object_name}: {e}")
            raise

    def delete_document(self, object_name: str) -> None:
        object_name = self._get_object_name(object_name)
        try:
            self.client.remove_object(self.bucket_name, object_name)
        except S3Error as e:
            logging.error(f"Delete error for {object_name}: {e}")
            raise
