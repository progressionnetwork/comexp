from datetime import datetime
from typing import Optional

from event.models import Event, EventRead
from sqlmodel import Field, Relationship, SQLModel


class PlanBase(SQLModel):
    name: str
    created_at: datetime


class Plan(PlanBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)
    events: Optional[list["Plan"]] = Relationship(back_populates="plan")


class PlanRead(PlanBase):
    id: int
    events: Optional[list["PlanEventRead"]]


class PlanEventBase(SQLModel):
    acc: float


class PlanEvent(PlanEventBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)

    plan_id: int | None = Field(default=None, foreign_key="plan.id")
    plan: Plan = Relationship(back_populates="events")

    event_id: int | None = Field(default=None, foreign_key="event.id")
    event: Event = Relationship(sa_relationship_kwargs={"lazy": "selectin"})


class PlanEventRead(PlanEventBase):
    id: int
    event: EventRead
