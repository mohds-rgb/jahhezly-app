# Evidence Register

Evidence in this repository is split into executable checks, source-only implementation status, and owner-reported history.

| Check | Result | Status |
|---|---|---|
| Backend pytest suite | `21 passed` | TESTED |
| Python compile / syntax validation | `compileall` successful for `app` and `migrations` | VERIFIED |
| Repository consistency validation | Latest run reported `REPOSITORY_VALIDATION_OK` | VERIFIED |
| Mobile source structure validation | `MOBILE_STRUCTURE_OK dart_files=26` | VERIFIED |
| Secret-pattern validation | included in repository validator; successful | VERIFIED |
| Alembic upgrade `0001 → 0002 → 0003 → 0004` | successful on temporary SQLite DB | TESTED |
| Alembic downgrade `0004 → 0003` and re-upgrade | successful | TESTED |
| Demo seed | 5 branches / 25 products / 5 active demo memberships | TESTED |
| Backend end-to-end smoke scenario | Catalog → guest order → idempotent replay → merchant accept → prepare → ready → collect | TESTED |
| Flutter analyze/build | Not executable in preparation environment because Flutter/Dart are unavailable | NOT VERIFIED |
| Android/iOS device testing | Not executed | NOT VERIFIED |
| PostgreSQL runtime | Not executed in preparation environment | NOT VERIFIED |
| Push notification provider | No external push provider is selected; the in-app/local notification boundary is implemented in source | PLANNED |
| WhatsApp external delivery | Not executed | NOT VERIFIED |
| Production deployment | Not executed | NOT CLAIMED |

## Owner-reported historical figures

The owner reports:

- 1,338 people
- 6 stores
- 3 orders
- 2 trials/experiments
- Successful / accepted outcome

No supporting artifacts or usage date were supplied. These figures are therefore **owner-reported and unverified** and are not used as independent production analytics.

## Evidence rule

A source implementation is not operational evidence. A claim becomes `TESTED` or `VERIFIED` only after an actual command/output is recorded here.
