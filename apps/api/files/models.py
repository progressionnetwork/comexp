from fastapi import File, UploadFile
from files.constants import FileType
from sqlmodel import Field, SQLModel


class FileDataBase(SQLModel):
    name: str
    file_type: FileType
    task_id: str | None


class FileData(FileDataBase, table=True):
    id: int = Field(primary_key=True, index=True, default=None)
    file_path: str | None


class FileDataCreate(FileDataBase):
    pass


class FileDataRead(FileDataBase):
    id: int
    status: str | None
    url: str | None


class FileDataUpdate(SQLModel):
    name: str | None
    file_type: FileType | None
    task_id: str | None
