from __future__ import annotations

from dataclasses import dataclass
import os

@dataclass(frozen=True)
class Settings:
    environment: str
    database_url: str
    jwt_secret: str
    jwt_expires_minutes: int
    allow_guest_orders: bool

    @classmethod
    def from_env(cls) -> "Settings":
        env = os.getenv("JAHHEZLY_ENV", "development")
        secret = os.getenv("JAHHEZLY_JWT_SECRET", "local-only-change-me")
        if env == "production" and (secret == "local-only-change-me" or len(secret.encode("utf-8")) < 32):
            raise RuntimeError("A JWT secret of at least 32 bytes is required in production.")
        return cls(
            environment=env,
            database_url=os.getenv("JAHHEZLY_DB_URL", "sqlite:///./jahhezly.db"),
            jwt_secret=secret,
            jwt_expires_minutes=int(os.getenv("JAHHEZLY_JWT_EXPIRES_MINUTES", "60")),
            allow_guest_orders=os.getenv("JAHHEZLY_ALLOW_GUEST_ORDERS", "true").lower() == "true",
        )

settings = Settings.from_env()
