from fastapi import HTTPException


def UnkownModelError(model: str, msg: str) -> HTTPException:
    return HTTPException(
        500,
        detail={"detail": [{"loc": ["model", model], "msg": msg}]},
    )
