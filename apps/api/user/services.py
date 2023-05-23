from auth.constants import PWD_CONTEXT
from pydantic import EmailStr
from share.exceptions import UnkownModelError
from share.services import get_one
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, or_, select
from user.models import User, UserCreate, UserRead


async def create(session: AsyncSession, user: UserCreate) -> UserRead:
    try:
        d_user = user.dict()
        d_user["hashed_password"] = PWD_CONTEXT.hash(user.password)
        del d_user["password"]
        db_user = User(**d_user)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
    except Exception as error:
        raise UnkownModelError(model="User", msg=str(error))
    return db_user


async def get_by_id(session: AsyncSession, id: int) -> UserRead:
    return await get_one(session=session, id=id, db_model=User)


async def get_by_email(session: AsyncSession, email: EmailStr) -> UserRead:
    try:
        statement = select(User).where(User.email == email)
        result = await session.execute(statement)
    except Exception as error:
        raise UnkownModelError(model="User", msg=str(error))
    return result.scalar_one_or_none()
