from celery import Celery
from config import settings

app = Celery("tasks", broker=settings.redis_url, backend=settings.redis_url)
# app.autodiscover_tasks(["tasks"])
import tasks.transcoding
