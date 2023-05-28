from celery.result import AsyncResult
from fastapi import Depends, File, UploadFile
from fastapi.responses import JSONResponse
from files.constants import FileType
from files.models import FileData, FileDataCreate, FileDataRead, FileDataUpdate
from files.services import create as file_create
from settings import get_settings
from share.database import get_session
from share.routers import CRUDRouter
from share.services import get_all as get_all_instances
from share.services import update as update_instance
from share.types import BoolResponse
from share.utils import pagination
from sqlalchemy.ext.asyncio import AsyncSession
from worker.tasks import update_from_file

router = CRUDRouter(
    create_model=FileDataCreate,
    read_model=FileDataRead,
    update_model=FileDataUpdate,
    db_model=FileData,
    update=False,
)


@router.get("/", response_model=list[FileDataRead], response_model_exclude_none=True)
async def route(
    session: AsyncSession = Depends(get_session),
    pagination: dict = Depends(pagination),
    # current_user=Depends(
    #     get_current_user_with_permmissions(model=self.db_model.__name__, type_permissions="read")
    # ),
) -> list[FileDataRead]:
    instances = await get_all_instances(
        session=session,
        offset=pagination.get("offset"),
        limit=pagination.get("limit"),
        db_model=FileData,
    )
    settings = get_settings()
    update_url_status = lambda row: FileDataRead(
        **(row.dict()),
        url=row.file_path.replace(settings.files_path, settings.media_url),
        status=(AsyncResult(row.task_id)).state if row.task_id is not None else "NEW"
    )

    instances = list(map(update_url_status, instances))

    return instances


@router.post("/", response_model=FileDataRead, response_model_exclude_none=True)
async def create(
    file_type: FileType,
    file: UploadFile = File(...),
    session: AsyncSession = Depends(get_session),
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    result = await file_create(session=session, file_type=file_type, file=file)
    return result


@router.get("/{id}/do", response_model=BoolResponse, response_model_exclude_none=True)
def do(
    id: int,
    session: AsyncSession = Depends(get_session),
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    task = update_from_file.delay(id)
    return BoolResponse(result=True)


@router.get("/file_type/", response_model_exclude_none=True)
def get_file_type(
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    return JSONResponse([i.value for i in FileType])
