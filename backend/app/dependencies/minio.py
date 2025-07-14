from app.clients.minio_client import MinioClient


minio_client = MinioClient()

def get_minio_client() -> MinioClient:
    return minio_client
