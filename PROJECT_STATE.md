# Project State

## Current phase
Phase 7 — Portfolio Release Candidate

## Current gate
G7/G8 preparation — source, backend correctness, migrations, repository controls, and evidence are hardened; mobile/device and production infrastructure remain unverified.

## Owner identity
- Mohammed Yaman ALdous
- GitHub: `mohds-rgb`
- https://github.com/mohds-rgb
- Email: `moydous@gmail.com`

## Product identity
- Jahhezly
- General retail Click & Collect
- Syria market scenario
- Arabic + English
- SYP
- Android + iOS target
- Guest browsing + optional customer identity
- Pickup contact phone retained only for order/contact needs

## Merchant scenario
- Paris Market — Basra, Daraa — one branch
- cham-center — Kafr Sousa, Damascus — four branches
- Owner states permission exists to use the business names in the public portfolio.

## Implementation status

| Area | Status |
|---|---|
| Product/domain baseline | IMPLEMENTED |
| Backend domain/API | IMPLEMENTED |
| Server authorization + multi-store membership | IMPLEMENTED |
| Catalog/price/availability | IMPLEMENTED |
| Orders/state machine | IMPLEMENTED |
| Idempotency | IMPLEMENTED |
| Optimistic concurrency | IMPLEMENTED |
| Audit events | IMPLEMENTED |
| Customer phone persistence | IMPLEMENTED |
| Backend tests | TESTED |
| Backend migrations through 0004 | TESTED |
| Backend end-to-end smoke scenario | TESTED |
| Flutter customer source | IMPLEMENTED |
| Flutter merchant source | IMPLEMENTED |
| Mobile source structure checks | VERIFIED |
| Flutter analyze/build/device | NOT VERIFIED IN THIS ENVIRONMENT |
| Offline cache/cart/queue source | IMPLEMENTED |
| Notification architecture | IMPLEMENTED AS IN-APP/LOCAL BOUNDARY; PUSH PROVIDER PLANNED |
| WhatsApp hand-off source | IMPLEMENTED |
| Programmable WhatsApp provider | PLANNED |
| PostgreSQL runtime | NOT VERIFIED IN THIS ENVIRONMENT |
| Production deployment | NOT CLAIMED |

## Owner-reported historical validation

- 1,338 people
- 6 stores
- 3 orders
- 2 trials
- Reported result: successful / accepted
- Usage date: not supplied
- Screenshots/logs/reports: none supplied
- Status: OWNER-REPORTED / UNVERIFIED

## Tests / verification actually executed

The current environment has verified the backend suite (`21 passed`), Python compilation, repository validation, mobile source-structure validation, secret-pattern validation, demo seeding (5 stores / 25 products / 5 memberships), the backend end-to-end smoke scenario, and Alembic upgrade/downgrade/re-upgrade checks through migration `0004`.

## Release status
NOT RELEASED.

No production users, revenue, uptime, app-store publication, signed APK/AAB, or external provider delivery is claimed by this repository.

## Known limitations
- Flutter/Dart and target mobile devices are unavailable in the preparation environment.
- PostgreSQL service runtime is unavailable in the preparation environment.
- Push provider credentials are intentionally absent.
- WhatsApp external delivery is not independently evidenced.
- Owner-reported historical usage metrics have no supporting artifacts.

## Next safe action
Run the local mobile verification matrix on a developer workstation with Flutter/Dart and target devices available; then run PostgreSQL-backed integration tests and produce a release artifact only when actual evidence exists.
