from datetime import datetime
from typing import Optional

from building.models import Building, BuildingRead, TypeBuildingFund
from event.models import Event, EventRead, SourceSystem
from sqlmodel import Field, Relationship, SQLModel
from work.models import WorkType, WorkTypeBase


class PlanEventBase(SQLModel):
    acc: float


class PlanEvent(PlanEventBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)

    plan_id: int | None = Field(default=None, foreign_key="plan.id")
    plan: "Plan" = Relationship(back_populates="events")

    building_id: int | None = Field(default=None, foreign_key="building.id")
    building: Building = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    event_id: int | None = Field(default=None, foreign_key="event.id")
    event: Event = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class PlanEventRead(PlanEventBase):
    id: int
    event: EventRead
    building: BuildingRead


class PlanWorkBase(SQLModel):
    acc: float
    start_day: float
    end_day: float


class PlanWork(PlanWorkBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)

    plan_id: int | None = Field(default=None, foreign_key="plan.id")
    plan: "Plan" = Relationship(back_populates="works")

    building_id: int | None = Field(default=None, foreign_key="building.id")
    building: Building = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    work_id: int | None = Field(default=None, foreign_key="worktype.id")
    work: WorkType = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class PlanWorkRead(PlanWorkBase):
    id: int
    work: WorkTypeBase
    building: BuildingRead


class PlanBase(SQLModel):
    name: str
    created_at: datetime = datetime.now()
    status: int = 0


class Plan(PlanBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)

    events: Optional[list[PlanEvent]] = Relationship(back_populates="plan")
    works: Optional[list[PlanWork]] = Relationship(back_populates="plan")


class PlanRead(PlanBase):
    id: int
    events: Optional[list[PlanEventRead]]
    works: Optional[list[PlanWorkRead]]
