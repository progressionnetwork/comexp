from datetime import date

from sqlmodel import Field, Relationship, SQLModel


class WorkTypeBase(SQLModel):
    name: str
    is_kr: bool = False


class WorkType(WorkTypeBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)


class WorkBase(SQLModel):
    period: int | None
    num_entrance: int | None
    num_elevator: int | None
    plan_date_start: date | None
    plan_date_end: date | None
    fact_date_start: date | None
    fact_date_end: date | None
    predict_date_start: date | None
    predict_date_end: date | None
    admarea: str | None
    district: str | None
    address: str | None
    building_id: int


class Work(WorkBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)
    work_type_id: int | None = Field(default=None, foreign_key="worktype.id")
    work_type: WorkType = Relationship(sa_relationship_kwargs={"lazy": "selectin"})
    building_id: int | None = Field(default=None, foreign_key="building.id")
    building: "Building" = Relationship(back_populates="works", sa_relationship_kwargs={"lazy": "selectin"})


class WorkRead(WorkBase):
    id: int
    work_type: WorkType
