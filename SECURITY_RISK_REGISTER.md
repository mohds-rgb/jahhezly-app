# Security Risk Register

| Threat | Asset | Primary control |
|---|---|---|
| IDOR | Orders/catalog | Server-side lookup and store scope |
| Tenant breakout | Merchant data | Membership + store authorization |
| Privilege escalation | Merchant operations | Role capability mapping |
| Price tampering | Commercial truth | Server price authority |
| Availability manipulation | Catalog | Manager-only mutation |
| Duplicate orders | Orders | Idempotency record |
| Replay | Mutations | Idempotency/state/version |
| Credential leakage | Secrets | Environment-only secret values |
| Token leakage | Sessions | No auth headers in structured logs |
| Order spam | Order creation | Future rate-limit boundary |
| Unsafe WhatsApp hand-off | Communication | Validated URL + explicit user action |
| Stale cache | Customer decisions | Freshness metadata |
