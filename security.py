import time
from typing import Annotated
from uuid import uuid4

import jwt
from fastapi import Depends, Request, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from exceptions import ForbiddenError, UnauthorizedError

SECRET = "fdae@15"
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    iss: str
    sub: int
    aud: str
    exp: float
    iat: float
    nbf: float
    jti: str


class JWTToken(BaseModel):
    access_token: AccessToken


def sign_jwt(user_id: int) -> JWTToken:
    now = time.time()
    payload = {
        "iss": "cars_fastapi.com.br",
        "sub": user_id,
        "aud": "cars_fastapi",
        "exp": now + (60 * 30),  # 30 minutes
        "iat": now,
        "nbf": now,
        "jti": uuid4().hex,
    }
    token = jwt.encode(payload, SECRET, algorithm=ALGORITHM)
    return {"access_token": token}


async def decode_jwt(token: str) -> JWTToken | None:
    try:
        decoded_token = jwt.decode(token, SECRET, audience="cars_fastapi", algorithms=[ALGORITHM])
        _token = JWTToken.model_validate({"access_token": decoded_token})
        return _token if _token.access_token.exp >= time.time() else None
    except Exception:
        return None


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> JWTToken:
        authorization = request.headers.get("Authorization", "")
        scheme, _, credentials = authorization.partition(" ")

        if credentials:
            if not scheme == "Bearer":
                raise UnauthorizedError("Invalid authentication scheme.")

            payload = await decode_jwt(credentials)
            if not payload:
                raise UnauthorizedError("Invalid or expired token.")
            return payload
        else:
            raise UnauthorizedError("Invalid authorization code.")


async def get_current_user(token: Annotated[JWTToken, Depends(JWTBearer())]) -> dict[str, int]:
    return {"user_id": token.access_token.sub}


def login_required(current_user: Annotated[dict[str, int], Depends(get_current_user)]):
    if not current_user:
        raise ForbiddenError("Access denied")
    return current_user
