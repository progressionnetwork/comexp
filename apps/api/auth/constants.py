from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from settings import get_settings
from user.constants import UserRole

settings = get_settings()

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_MINUTES = settings.refresh_token_expire_minutes
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/signin")

PERMISSIONS = {
    UserRole.ADMIN: {
        "User": {
            "read": True,
            "write": True,
            "delete": True,
        },
    },
    UserRole.USER: {
        "User": {
            "read": False,
            "write": False,
            "delete": False,
        },
    },
}
