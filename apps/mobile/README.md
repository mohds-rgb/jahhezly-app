# Jahhezly Mobile

Flutter customer + merchant mobile client source for Jahhezly.

## Implemented in source

- Offline-capable catalog repository with store-scoped freshness metadata.
- SQLite-backed store-scoped cart and durable synchronization queue.
- Explicit queued-for-submission vs authoritative server-order states.
- Versioned local schema through version `4` with additive, non-destructive migrations.
- REST client with structured error decoding.
- Customer phone capture for pickup contact.
- Customer catalog, product details, cart review, submission, and order-status surfaces.
- Merchant login, server-provided branch membership selection, and order workflow operations.
- Arabic RTL and English LTR presentation foundation.
- WhatsApp user-controlled hand-off using a `wa.me` URL.

## Local data guarantees

Catalog cache and cart rows are scoped by store so changing branches cannot accidentally read another branch's cached catalog or cart through normal repository APIs. Offline drafts remain local until an authoritative backend response exists.

## Verification boundary

Flutter/Dart was not installed in the preparation environment. Therefore the mobile package is **implemented in source and structurally checked, but not compiled, analyzed, or device-tested here**.

## Expected commands

```bash
flutter pub get
flutter analyze
flutter test
flutter run
```

The mobile package intentionally contains no production credentials, signing keys, or provider secrets.
