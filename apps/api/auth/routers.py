from auth.constants import oauth2_scheme
from auth.dependencies import get_current_active_user
from auth.models import SignIn, SignUp, Token
from auth.services import signin as auth_signin
from auth.services import signup as auth_signup
from auth.services import update_tokens as auth_update_tokens
from fastapi import APIRouter, Depends, HTTPException, Query
from share.database import get_session
from user.models import UserCreate, UserRead

router = APIRouter()


@router.post("/signup", response_model=UserRead)
async def signup(data: SignUp, session=Depends(get_session)):
    return await auth_signup(data=data, session=session)


@router.post("/signin", response_model=Token)
async def signin(data: SignIn = Depends(), session=Depends(get_session)):
    return await auth_signin(data=data, session=session)


@router.post("/update_token", response_model=Token)
async def update_tokens(current_active_user=Depends(get_current_active_user), session=Depends(get_session)):
    return await auth_update_tokens(user=current_active_user, session=session)
