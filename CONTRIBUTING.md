# Contributing

Preserve these invariants:

- server-authoritative pricing
- server-enforced merchant authorization
- order state-machine transitions
- idempotent order submission
- durable local state
- migration discipline
- no secrets in source control

Before changes:

```bash
python scripts/validate_repo.py
cd backend && pytest -q
```

Run Flutter analyze/tests when a Flutter SDK is available.
