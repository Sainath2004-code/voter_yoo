import os
from celery import Celery

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

def create_celery_app(service_name: str):
    app = Celery(
        service_name,
        broker=REDIS_URL,
        backend=REDIS_URL
    )
    
    app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='Asia/Kolkata',
        enable_utc=True,
        task_track_started=True,
        task_time_limit=300, # 5 minutes
    )
    
    return app
