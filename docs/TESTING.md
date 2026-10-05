# Testing Strategy

Jahhezly focuses automated testing on the highest-value correctness boundaries: pricing, availability, authorization, order state transitions, idempotency, concurrency, migration behavior, and input validation.

## Current automated coverage

The backend suite covers:

- password hashing and verification;
- public catalog access;
- server-side price validation;
- historical price preservation;
- unavailable products;
- duplicate order prevention through idempotency;
- idempotency-key reuse with a different payload;
- guest order ownership;
- customer phone validation and persistence;
- optimistic concurrency on merchant transitions;
- customer cancellation version checks;
- terminal-state protection;
- cross-store authorization;
- invalid token handling;
- multi-branch memberships;
- inconsistent organization membership rejection.

The mobile repository also contains domain-level tests for the order state machine and the WhatsApp adapter, plus a static source-structure validator that checks relative imports and declared assets.

## Actual evidence

The preparation environment executed the backend tests successfully (`20 passed`), Python compilation, the repository validator, the mobile structure validator, and an Alembic upgrade/downgrade/re-upgrade cycle through migration `0004`.

Flutter analysis, Flutter tests, Android/iOS builds, device testing, and PostgreSQL runtime tests require a developer environment with those toolchains and are therefore explicitly left as `NOT VERIFIED` here.

## Suggested local verification sequence

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
python -m compileall -q app migrations

# Repository + mobile structure
cd ..
python scripts/validate_repo.py
python scripts/validate_mobile_structure.py

# Mobile (developer workstation)
cd apps/mobile
flutter pub get
flutter analyze
flutter test
flutter run
```
