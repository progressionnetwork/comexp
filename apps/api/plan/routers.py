from fastapi import Depends
from plan.models import (
    Plan,
    PlanBase,
    PlanEvent,
    PlanEventBase,
    PlanEventRead,
    PlanRead,
    PlanWork,
    PlanWorkBase,
    PlanWorkRead,
)
from plan.services import create as create_plan
from share.database import get_session
from share.routers import CRUDRouter
from sqlalchemy.ext.asyncio import AsyncSession

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
