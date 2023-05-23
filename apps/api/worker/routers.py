from celery.result import AsyncResult
from fastapi import APIRouter

router = APIRouter()


@router.get("/{task_id}")
async def result(task_id: str):
    task = AsyncResult(task_id)
    if not task.ready():
        return {"status": task.status}
    task_result = task.get()
    return {"task_id": str(task_id), "result": task_result, "tast_result": task.status, "task_r": task.result}
