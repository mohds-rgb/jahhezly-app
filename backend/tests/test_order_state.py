from app.domain.order import can_transition

def test_allowed_path():
    assert can_transition("SUBMITTED","ACCEPTED")
    assert can_transition("ACCEPTED","PREPARING")
    assert can_transition("PREPARING","READY_FOR_PICKUP")
    assert can_transition("READY_FOR_PICKUP","COLLECTED")

def test_terminal_cannot_reopen():
    assert not can_transition("COLLECTED","PREPARING")
    assert not can_transition("REJECTED","ACCEPTED")
    assert not can_transition("CANCELLED","ACCEPTED")

def test_invalid_path():
    assert not can_transition("SUBMITTED","READY_FOR_PICKUP")
