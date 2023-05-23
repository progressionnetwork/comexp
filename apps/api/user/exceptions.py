from fastapi import HTTPException, status


class UserNotExist(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="A user not exists")


class UserUknownError(HTTPException):
    def __init__(self, error: str) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=error,
        )
