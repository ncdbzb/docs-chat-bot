import io
from minio import Minio
from minio.error import S3Error

from app.config import settings
from app.logger import logger


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
                logger.info(f"Bucket '{self.bucket_name}' создан в MinIO")
            else:
                logger.info(f"Bucket '{self.bucket_name}' уже существует в MinIO")
        except S3Error as e:
            logger.exception(f"Ошибка инициализации MinIO bucket: {e}")
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
            logger.info(f"Файл успешно загружен в MinIO: {object_name}")
        except S3Error as e:
            logger.error(f"Ошибка загрузки {object_name} в MinIO: {e}")
            raise

    def delete_document(self, object_name: str) -> None:
        object_name = self._get_object_name(object_name)
        try:
            self.client.remove_object(self.bucket_name, object_name)
            logger.info(f"Файл успешно удалён из MinIO: {object_name}")
        except S3Error as e:
            logger.error(f"Ошибка удаления {object_name} из MinIO: {e}")
            raise

    def list_documents(self) -> list[str]:
        prefix = f"{self.root_path}/" if self.root_path else ""
        try:
            objects = self.client.list_objects(bucket_name=self.bucket_name, prefix=prefix, recursive=True)
            object_names = [obj.object_name for obj in objects]
            logger.info(f"Получено {len(object_names)} объектов из MinIO с префиксом '{prefix}'")
            return object_names
        except S3Error as e:
            logger.error(f"Ошибка при получении списка объектов из MinIO: {e}")
            raise
