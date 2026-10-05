import json
import uuid
from sqlalchemy.orm import Session
from ..models import AuditEvent

def record_audit(db: Session, *, actor_id, organization_id, store_id, aggregate_id, action,
                 before=None, after=None, correlation_id):
    db.add(AuditEvent(
        id=str(uuid.uuid4()),
        actor_id=actor_id,
        organization_id=organization_id,
        store_id=store_id,
        aggregate_id=aggregate_id,
        action=action,
        before_summary=json.dumps(before, sort_keys=True) if before else None,
        after_summary=json.dumps(after, sort_keys=True) if after else None,
        correlation_id=correlation_id,
    ))
