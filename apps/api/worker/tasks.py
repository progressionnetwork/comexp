from files.constants import FileType
from worker.app import celery_app
from worker.services import predict_works_and_incidents
from worker.services import update_from_file as task_update_from_file


@celery_app.task(bind=True)
def update_from_file(self, id: int):
    return task_update_from_file(id=id, task=self)


@celery_app.task(bind=True)
def predict(self, id: int, street: str, source_id: int, type_fund_id: str, date_start: str, date_end: str):
    return predict_works_and_incidents(
        id=id,
        task=self,
        street=street,
        source_id=source_id,
        type_fund_id=type_fund_id,
        date_start=date_start,
        date_end=date_end,
    )
