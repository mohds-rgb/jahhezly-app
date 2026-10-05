# Risk Register

| ID | Risk | Severity | Control | Status |
|---|---|---:|---|---|
| R-01 | Owner decisions unresolved | High | OPEN_QUESTIONS | Open |
| R-02 | Stale client price becomes final | Critical | Server price validation | Controlled |
| R-03 | Duplicate submission | Critical | Idempotency key + unique constraint | Controlled |
| R-04 | Cross-store access | Critical | Server membership/store scope | Controlled |
| R-05 | Concurrent merchant updates | High | Version check + conditional update | Controlled |
| R-06 | Draft appears confirmed | Critical | Explicit local states | Controlled |
| R-07 | WhatsApp hand-off misrepresented | High | Adapter does not change order state | Controlled |
| R-08 | Migration data loss | Critical | Versioned schema upgrade/migration | Baseline |
| R-09 | Secret enters repo | Critical | env-only config + validator | Controlled |
| R-10 | Mobile not verified here | Medium | Honest status + CI mobile job | Open |
