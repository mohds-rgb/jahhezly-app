from datetime import datetime, timedelta, timezone
import jwt

from ..config import settings

ALGORITHM = "HS256"

def create_access_token(subject: str):
    expires_in = settings.jwt_expires_minutes * 60
    now = datetime.now(timezone.utc)
    token = jwt.encode(
        {"sub": subject, "typ": "merchant_access", "iat": now, "exp": now + timedelta(seconds=expires_in)},
        settings.jwt_secret,
        algorithm=ALGORITHM,
    )
    return token, expires_in

def decode_access_token(token: str):
    payload = jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[ALGORITHM],
        options={"require": ["sub", "iat", "exp"]},
    )
    if payload.get("typ") != "merchant_access":
        raise jwt.InvalidTokenError("Unexpected token type")
    return str(payload["sub"])
