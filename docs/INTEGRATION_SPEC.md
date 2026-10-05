# Integration Specification

## WhatsApp V1

```text
validated order data
    ↓
message formatter
    ↓
user-controlled wa.me link
    ↓
user launches WhatsApp
    ↓
user reviews / sends
```

Opening the composer is **not** delivery evidence. The order remains authoritative in Jahhezly.

## Notifications

Order-state changes are surfaced by the in-app order-status workflow. A future push adapter may subscribe to authoritative state changes, but no push provider is embedded or claimed in this portfolio release.

## Future programmable WhatsApp integration

Requires an owner-approved provider, provider-specific credentials, webhook verification, template rules where applicable, delivery evidence, privacy analysis, cost governance, and outage handling. It is not implemented here.
