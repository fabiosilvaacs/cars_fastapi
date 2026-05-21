from pydantic import BaseModel


class LoginIn(BaseModel):
    user_id: int


class LoginOut(BaseModel):
    access_token: str
