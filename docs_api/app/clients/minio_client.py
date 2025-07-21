import io
from minio import Minio
from minio.error import S3Error

from app.config import settings
from app.logger import logger


class MinioClient():
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
                logger.info(f"Bucket '{self.bucket_name}' создан в MinIO")
            else:
                logger.info(f"Bucket '{self.bucket_name}' уже существует в MinIO")
        except S3Error as e:
            logger.exception(f"Ошибка инициализации MinIO bucket: {e}")
            raise
    
    def _get_object_name(self, filename: str) -> str:
        return f"{self.root_path}/{filename}" if self.root_path else filename
    
    def get_document(self, object_name: str) -> bytes:
        """
        Получает документ из MinIO по имени объекта и возвращает его содержимое в виде байтов.
        """
        object_name = self._get_object_name(object_name)
        try:
            response = self.client.get_object(bucket_name=self.bucket_name, object_name=object_name)
            file_bytes = response.read()
            logger.info(f"Файл успешно получен из MinIO: {object_name}")
            return file_bytes
        except S3Error as e:
            logger.error(f"Ошибка получения {object_name} из MinIO: {e}")
            raise
        finally:
            response.close()
            response.release_conn()
