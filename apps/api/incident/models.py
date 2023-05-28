from datetime import datetime

from event.models import Event, EventRead
from sqlmodel import Field, Relationship, SQLModel


class IncidentBase(SQLModel):
    date_system_create: datetime | None
    date_system_close: datetime | None
    date_close: datetime | None


class Incident(IncidentBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)

    event_id: int | None = Field(default=None, foreign_key="event.id")
    event: Event = Relationship(sa_relationship_kwargs={"lazy": "selectin"})

    building_id: int | None = Field(default=None, foreign_key="building.id")
    building: "Building" = Relationship(back_populates="incidents", sa_relationship_kwargs={"lazy": "selectin"})


class IncidentRead(IncidentBase):
    id: int
    event: EventRead
    building_id: int
