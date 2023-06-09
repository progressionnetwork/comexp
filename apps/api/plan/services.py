from datetime import datetime

from building.models import Building
from event.models import SourceSystem
from plan.models import Plan, PlanEvent, PlanRead, PlanWork
from share.services import get_one as get_plan
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


async def get_file(id: int, session: AsyncSession):
    import io

    import pandas as pd

    statement = select(PlanWork).where(PlanWork.plan_id == id)
    result = await session.execute(statement)
    plan_works = result.scalars().all()
    plan_works = [plan_work.dict() for plan_work in plan_works]

    statement = select(PlanEvent).where(PlanEvent.plan_id == id)
    result = await session.execute(statement)
    plan_events = result.scalars().all()
    plan_events = [plan_event.dict() for plan_event in plan_events]

    df_works = pd.DataFrame.from_records(plan_works)
    df_events = pd.DataFrame.from_records(plan_events)
    in_memory_fp = io.BytesIO()
    with pd.ExcelWriter(
        in_memory_fp,
    ) as writer:
        df_works.to_excel(writer, index=False, sheet_name="Works")
        df_events.to_excel(writer, index=False, sheet_name="Events")
    in_memory_fp.seek(0, 0)
    return in_memory_fp
