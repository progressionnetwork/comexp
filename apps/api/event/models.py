from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class EventBase(SQLModel):
    name: str | None


class Event(EventBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)

    source_id: int | None = Field(default=None, foreign_key="sourcesystem.id")
    source: "SourceSystem" = Relationship(back_populates="events", sa_relationship_kwargs={"lazy": "selectin"})


class SourceSystemBase(SQLModel):
    name: str | None


class SourceSystem(SourceSystemBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)
    events: Optional[List[Event]] = Relationship(back_populates="source", sa_relationship_kwargs={"lazy": "selectin"})


class SourceSystemShortRead(SourceSystemBase):
    id: int


class EventNested(EventBase):
    id: int


class SourceSystemRead(SourceSystemBase):
    id: int
    events: Optional[list[EventNested]]


class EventRead(EventBase):
    id: int
    source: SourceSystemShortRead
