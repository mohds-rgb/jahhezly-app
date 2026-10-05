from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ...db import get_db
from ...domain.errors import DomainError
from ...models import StaffUser
from ...schemas import LoginRequest, LoginResponse
from ...security.passwords import verify_password
from ...security.tokens import create_access_token

router = APIRouter(prefix="/v1/auth", tags=["auth"])

@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.scalar(select(StaffUser).where(StaffUser.email == payload.email.lower().strip()))
    if not user or not user.active or not verify_password(payload.password, user.password_hash):
        raise DomainError("UNAUTHORIZED", "Invalid credentials.", status=401)
    token, expires = create_access_token(user.id)
    return LoginResponse(accessToken=token, tokenType="bearer", expiresIn=expires)
