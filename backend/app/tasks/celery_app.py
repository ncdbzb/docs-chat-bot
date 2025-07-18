from celery import Celery

from app.config import settings


celery_app = Celery(
    'tasks',
    broker=settings.redis_url,
    result_backend=settings.redis_url,
    include=['app.tasks.email_task']
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Yekaterinburg',
    enable_utc=True,
)
