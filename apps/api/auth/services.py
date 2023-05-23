from datetime import datetime, timedelta
from uuid import uuid4

from auth.constants import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, PWD_CONTEXT, REFRESH_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from auth.exceptions import InvalidCredentials, UserIsNotActive, VerifyError
from auth.models import SignIn, SignUp, Token
from jose import jwt
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from user.constants import UserRole
from user.exceptions import UserNotExist
from user.models import User, UserCreate, UserRead
from user.services import create as user_create
from user.services import get_by_email as get_user_by_email


async def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


async def _authenticate(email: EmailStr, password: str, session: AsyncSession):
    user: User = await get_user_by_email(session=session, email=email)
    if user is None:
        raise UserNotExist
    else:
        if not await _verify_password(password, user.hashed_password):
            raise InvalidCredentials
    if not user.is_active:
        raise UserIsNotActive
    return user


def _create_access_token(subject: int, expires_delta: timedelta | None = None) -> Token:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _create_refresh_token(subject: int, expires_delta: timedelta | None = None) -> Token:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def signup(data: SignUp, session: AsyncSession) -> UserRead:
    verify_code_phone = uuid4()
    schema_user_create = UserCreate(
        is_active=False,
        verify_code_phone=str(verify_code_phone),
        created=datetime.utcnow(),
        role=UserRole.GAMER,
        **(data.dict()),
    )
    new_user = await user_create(user=schema_user_create, session=session)
    return new_user


async def signin(data: SignIn, session: AsyncSession) -> Token:
    user = await _authenticate(email=data.email, password=data.password, session=session)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(user.id, expires_delta=access_token_expires)
    refresh_token = _create_refresh_token(user.id, expires_delta=refresh_token_expires)
    return Token(
        access_token=access_token,
        access_token_expired_at=datetime.utcnow() + access_token_expires,
        token_type="bearer",
        refresh_token=refresh_token,
        refresh_token_expired_at=datetime.utcnow() + refresh_token_expires,
        user=user,
    )


async def update_tokens(user: User, session: AsyncSession) -> Token:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    access_token = _create_access_token(user.id, expires_delta=access_token_expires)
    refresh_token = _create_refresh_token(user.id, expires_delta=refresh_token_expires)
    return Token(
        access_token=access_token,
        access_token_expired_at=datetime.utcnow() + access_token_expires,
        token_type="bearer",
        refresh_token=refresh_token,
        refresh_token_expired_at=datetime.utcnow() + refresh_token_expires,
        user=user,
    )
