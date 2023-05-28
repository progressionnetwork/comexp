from datetime import datetime

from share.exceptions import UnkownModelError
from share.types import BoolResponse
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import SQLModel, func, select


async def create(session: AsyncSession, create_model: SQLModel, db_model: SQLModel) -> SQLModel:
    try:
        dict_model = create_model.dict()
        instance = db_model(**dict_model)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
    except Exception as error:
        raise UnkownModelError(model=db_model.__name__, msg=str(error))
    return instance


async def get_one(session: AsyncSession, id: int, db_model: SQLModel) -> SQLModel:
    try:
        statement = select(db_model).where(db_model.id == id)
        result = await session.execute(statement)
    except Exception as error:
        raise UnkownModelError(model=db_model.__name__, msg=str(error))
    return result.scalar_one_or_none()


async def get_all(session: AsyncSession, db_model: SQLModel, offset: int = 0, limit: int = 0) -> list[SQLModel]:
    try:
        statement = select(db_model).offset(offset).limit(limit)
        result = await session.execute(statement)
    except Exception as error:
        raise UnkownModelError(model=db_model.__name__, msg=str(error))
    return result.scalars().all()


async def count(session: AsyncSession, db_model: SQLModel) -> int:
    try:
        print(f"{func.count(db_model.id)=}")
        statement = select(func.count(db_model.id))
        print(f"sss")
        result = await session.execute(statement)
    except Exception as error:
        raise UnkownModelError(model=db_model.__name__, msg=str(error))
    return result.scalars().one()


async def update(session: AsyncSession, id: int, update_model: SQLModel, db_model: SQLModel) -> SQLModel:
    try:
        instance = await get_one(session=session, id=id, db_model=db_model)
        dict_model = update_model.dict()
        for key in list(dict_model.keys()):
            if (value := dict_model.get(key)) is not None:
                setattr(instance, key, value)
        if instance.dict().get("update_at") is not None:
            instance.update_at = datetime.utcnow()
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
    except Exception as error:
        raise UnkownModelError(model=db_model.__name__, msg=str(error))
    return instance


async def delete_one(session: AsyncSession, id: int, db_model: SQLModel) -> BoolResponse:
    try:
        instance = await get_one(session=session, id=id, db_model=db_model)
        await session.delete(instance)
        await session.commit()
        return BoolResponse(result=True)
    except Exception as error:
        raise UnkownModelError(model=db_model.__name__, msg=str(error))


async def delete_all(session: AsyncSession, db_model: SQLModel) -> BoolResponse:
    try:
        await session.query(db_model).delete()
        await session.commit()
        return BoolResponse(result=True)
    except Exception as error:
        raise UnkownModelError(model=db_model.__name__, msg=str(error))
