from files.constants import FileType
from worker.app import celery_app
from worker.services import update_from_file as task_update_from_file


@celery_app.task(bind=True)
def update_from_file(self, id: int):
    return task_update_from_file(id=id, task=self)
