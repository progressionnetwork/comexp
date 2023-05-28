from datetime import datetime

from building.models import Building
from event.models import SourceSystem
from plan.models import Plan, PlanRead
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import col, select
from worker.tasks import predict


async def create(
    street: str, type_fund_id: int, sourcesystem_id: int, date_start: str, date_end: str, session: AsyncSession
) -> PlanRead:
    plan = Plan(
        name=f"Планировние от {datetime.now()}",
    )
    session.add(plan)
    await session.commit()
    await session.refresh(plan)
    predict.delay(
        id=plan.id,
        street=street,
        source_id=sourcesystem_id,
        type_fund_id=type_fund_id,
        date_start=date_start,
        date_end=date_end,
    )

    return PlanRead(**(plan.dict()))
