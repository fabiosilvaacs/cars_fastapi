from fastapi import APIRouter

from security import sign_jwt
from models.auth import LoginIn, LoginOut

router = APIRouter(prefix="/auth")


@router.post("/login", response_model=LoginOut)
async def login(data: LoginIn):
    return sign_jwt(user_id=data.user_id)
