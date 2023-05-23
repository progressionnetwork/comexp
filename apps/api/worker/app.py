import os

from celery import Celery

celery_app = Celery(
    "worker",
    broker_url=os.getenv("CELERY_BROKER_URL"),
    result_backend=os.getenv("CELERY_RESULT_BACKEND"),
)


celery_app.conf.update(task_track_started=True)
