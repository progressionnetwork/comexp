from auth.dependencies import get_current_active_user, get_user_with_required_roles
from fastapi import APIRouter, Depends
from share.database import get_session
from share.routers import CRUDRouter
from sqlalchemy.ext.asyncio import AsyncSession
from user.constants import UserRole
from user.models import User, UserCreate, UserRead, UserUpdate
from user.services import create as user_create

router = CRUDRouter(
    create_model=UserCreate, read_model=UserRead, update_model=UserUpdate, db_model=User, delete_all=False, create=False
)


@router.post("/", response_model=UserRead, summary="Create one record")
async def create(user: UserCreate, session: AsyncSession = Depends(get_session)):
    return await user_create(user=user, session=session)


@router.get("/me/", response_model=UserRead)
async def me(current_user: UserRead = Depends(get_current_active_user)):
    return current_user
