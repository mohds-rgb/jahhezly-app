# Operations Runbook

Design baseline only; not a deployment claim.

## API outage
Preserve local drafts. Never show a local draft as confirmed.

## Duplicate order
Inspect idempotency record, request hash, order and audit events before remediation.

## Price manipulation
Inspect price history, audit actor and order item snapshot.

## Merchant account takeover
Disable the staff identity, preserve evidence, review membership changes and rotate secrets as appropriate.

## Migration failure
Preserve migration version/process evidence and resume only through a documented path.

## WhatsApp issue
Do not roll back the authoritative order because WhatsApp is unavailable.
