from pydantic import BaseModel


class BoolResponse(BaseModel):
    result: bool
