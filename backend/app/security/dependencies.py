from dataclasses import dataclass
import jwt
from fastapi import Depends, Header
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..domain.errors import DomainError, forbidden
from ..models import StaffMembership, StaffUser, Store
from .tokens import decode_access_token

bearer = HTTPBearer(auto_error=False)

@dataclass(frozen=True)
class StaffContext:
    user: StaffUser
    memberships: tuple[StaffMembership, ...]

    def membership_for(self, store_id: str) -> StaffMembership | None:
        return next((m for m in self.memberships if m.store_id == store_id), None)

ROLE_CAPABILITIES = {
    "STORE_OPERATOR": {"view_orders", "transition_orders"},
    "STORE_MANAGER": {"view_orders", "transition_orders", "manage_catalog", "manage_prices", "manage_availability"},
    "MERCHANT_ADMIN": {"view_orders", "transition_orders", "manage_catalog", "manage_prices", "manage_availability", "manage_staff"},
}

def get_current_staff(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
    db: Session = Depends(get_db),
):
    if credentials is None:
        raise DomainError("UNAUTHORIZED", "Authentication is required.", status=401)
    try:
        staff_id = decode_access_token(credentials.credentials)
    except (jwt.InvalidTokenError, ValueError):
        raise DomainError("UNAUTHORIZED", "Authentication token is invalid.", status=401)
    user = db.get(StaffUser, staff_id)
    if not user or not user.active:
        raise DomainError("UNAUTHORIZED", "Staff account is inactive or unknown.", status=401)
    memberships = tuple(db.scalars(
        select(StaffMembership).join(Store, Store.id == StaffMembership.store_id).where(
            StaffMembership.user_id == user.id,
            StaffMembership.active.is_(True),
            Store.active.is_(True),
            Store.organization_id == StaffMembership.organization_id,
        ).order_by(StaffMembership.store_id)
    ).all())
    if not memberships:
        raise forbidden("No active merchant membership is available for this user.")
    return StaffContext(user=user, memberships=memberships)

def require_capability(capability, store_id, context: StaffContext):
    membership = context.membership_for(store_id)
    if membership is None:
        raise forbidden("You are not authorized for this store.")
    if capability not in ROLE_CAPABILITIES.get(membership.role, set()):
        raise forbidden("Your role cannot perform this operation.")
    return membership

def expected_version_header(value: str | None = Header(default=None, alias='If-Match')):
    if value is None:
        raise DomainError("INVALID_REQUEST", "If-Match version is required.", status=422)
    try:
        return int(value)
    except ValueError:
        raise DomainError("INVALID_REQUEST", "If-Match must be an integer.", status=422)
