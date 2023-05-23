from pydantic import EmailStr
from share.models import ModelWithDateCreateAndUpdate
from sqlmodel import Field, Relationship, SQLModel
from user.constants import UserRole


class UserBase(SQLModel):
    first_name: str = Field(min_length=4, max_length=128)
    last_name: str = Field(min_length=4, max_length=128)
    email: EmailStr
    role: UserRole


class User(UserBase, ModelWithDateCreateAndUpdate, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    hashed_password: str
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase, ModelWithDateCreateAndUpdate):
    id: int
    is_active: bool


class UserUpdate(SQLModel):
    first_name: str | None = Field(min_length=4, max_length=128)
    last_name: str | None = Field(min_length=4, max_length=128)
    email: EmailStr | None
    role: UserRole | None
