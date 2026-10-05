from enum import StrEnum

class OrderState(StrEnum):
    DRAFT = "DRAFT"
    PENDING_SUBMISSION = "PENDING_SUBMISSION"
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    PREPARING = "PREPARING"
    READY_FOR_PICKUP = "READY_FOR_PICKUP"
    COLLECTED = "COLLECTED"
    REJECTED = "REJECTED"
    CANCELLED = "CANCELLED"

SERVER_TRANSITIONS = {
    OrderState.SUBMITTED: {OrderState.ACCEPTED, OrderState.REJECTED, OrderState.CANCELLED},
    OrderState.ACCEPTED: {OrderState.PREPARING, OrderState.CANCELLED},
    OrderState.PREPARING: {OrderState.READY_FOR_PICKUP, OrderState.CANCELLED},
    OrderState.READY_FOR_PICKUP: {OrderState.COLLECTED, OrderState.CANCELLED},
    OrderState.COLLECTED: set(),
    OrderState.REJECTED: set(),
    OrderState.CANCELLED: set(),
    OrderState.DRAFT: set(),
    OrderState.PENDING_SUBMISSION: set(),
}

def can_transition(current: str, target: str) -> bool:
    try:
        current_state = OrderState(current)
        target_state = OrderState(target)
    except ValueError:
        return False
    return target_state in SERVER_TRANSITIONS.get(current_state, set())
