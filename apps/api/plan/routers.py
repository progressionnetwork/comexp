from fastapi import Depends
from fastapi.responses import JSONResponse, StreamingResponse
from plan.models import (
    Plan,
    PlanBase,
    PlanEvent,
    PlanEventBase,
    PlanEventRead,
    PlanMinimal,
    PlanRead,
    PlanReadShort,
    PlanWork,
    PlanWorkBase,
    PlanWorkRead,
)
from plan.services import create as create_plan
from plan.services import get_file as get_file_from_db
from share.database import get_session
from share.exceptions import UnkownModelError
from share.routers import CRUDRouter
from share.services import get_all as get_all_instances
from share.utils import pagination
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from sqlmodel import col, select
from worker.tasks import predict

router = CRUDRouter(create_model=PlanBase, read_model=PlanRead, update_model=PlanBase, db_model=Plan, create=False)
router_event = CRUDRouter(
    create_model=PlanEventBase, read_model=PlanEventRead, update_model=PlanEventBase, db_model=PlanEvent
)
router_work = CRUDRouter(
    create_model=PlanWorkBase, read_model=PlanWorkRead, update_model=PlanWorkBase, db_model=PlanWork
)


@router.post("/", response_model=PlanRead, response_model_exclude_none=True)
async def create(
    street: str,
    type_fund_id: int,
    sorucesystem_id: int,
    start_date: str,
    end_date: str,
    session: AsyncSession = Depends(get_session),
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    result = await create_plan(
        street=street,
        session=session,
        type_fund_id=type_fund_id,
        sourcesystem_id=sorucesystem_id,
        date_start=start_date,
        date_end=end_date,
    )
    return result


@router.get("/", response_model=list[PlanReadShort], response_model_exclude_none=True)
async def get_all(
    pagination: dict = Depends(pagination),
    session: AsyncSession = Depends(get_session),
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    try:
        statement = select(PlanMinimal).limit(pagination.get("limit"))
        result = await session.execute(statement)
    except Exception as error:
        raise UnkownModelError(model="Plan", msg=str(error))
    return result.scalars().all()


@router.get("/{id}/xlsx", response_model=list[PlanReadShort], response_model_exclude_none=True)
async def get_file(
    id: int,
    session: AsyncSession = Depends(get_session),
    # current_user=Depends(get_current_user_with_permmissions(model="OKPD2", type_permissions="read")),
):
    output = await get_file_from_db(id=id, session=session)
    headers = {
        "Content-Disposition": 'attachment; filename="export.xlsx"',
        "Content-Type": "vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }
    return StreamingResponse(output, headers=headers)
