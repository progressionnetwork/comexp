from datetime import datetime

from sqlmodel import Field, SQLModel


class ModelWithDateCreateAndUpdate(SQLModel):
    created_at: datetime = Field(default=datetime.utcnow(), nullable=False)
    update_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
