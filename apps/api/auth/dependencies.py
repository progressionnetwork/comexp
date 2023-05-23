from auth.constants import ALGORITHM, PERMISSIONS, SECRET_KEY, oauth2_scheme
from auth.exceptions import InvalidCredentials, PermissionDenied, TokenExpired, UserIsNotActive
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from share.database import get_session
from sqlalchemy.orm import Session
from user.constants import UserRole
from user.models import User, UserRead
from user.services import get_by_id as get_user_by_id


async def get_current_user(token: str = Depends(oauth2_scheme), session=Depends(get_session)) -> UserRead:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = int(payload.get("sub"))
        if user_id is None or payload.get("type") != "access":
            raise InvalidCredentials
    except JWTError as err:
        raise TokenExpired
    user = await get_user_by_id(session=session, id=user_id)
    if user is None:
        raise InvalidCredentials
    return user


async def get_current_active_user(current_user: UserRead = Depends(get_current_user)):
    if not current_user.is_active:
        raise UserIsNotActive
    return current_user


def get_user_with_required_roles(roles: list[UserRole]):
    async def have_roles(current_active_user: UserRead = Depends(get_current_active_user)):
        if current_active_user.role not in roles:
            raise PermissionDenied
        return current_active_user

    return have_roles


def get_current_user_with_permmissions(type_permissions: str, model: str):
    async def has_perm(current_user: UserRead = Depends(get_current_active_user)):
        if not PERMISSIONS[current_user.role][model][type_permissions]:
            raise PermissionDenied
        return PERMISSIONS[current_user.role][model][type_permissions]

    return has_perm
