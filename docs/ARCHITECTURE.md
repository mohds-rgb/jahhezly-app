# Architecture

## System boundary

```text
Flutter mobile
    ↓ HTTPS
FastAPI modular monolith
    ↓
application services
    ↓
domain rules
    ↓
SQLAlchemy
    ↓
PostgreSQL
```

SQLite is used for backend automated tests. The customer mobile layer also uses SQLite for store-scoped catalog cache, cart state, and durable synchronization metadata.

## Domain

### Catalog
Product identity, historical price records, explicit availability, store ownership.

### Orders
Order aggregate, immutable item snapshots, state machine, idempotency and customer-session ownership.

### Authorization
JWT identifies the staff user. The server resolves store membership and capabilities from authoritative data.

### Offline
Local storage contains cached catalog data, freshness metadata, draft cart and queued submissions. It never overrides final price, availability, authorization, order state or pickup state.

### WhatsApp
The adapter formats a message and opens a user-controlled `wa.me` link. It does not mark the order delivered.

## Concurrency
Merchant transitions use `If-Match` version checks and conditional updates:

```text
current state + expected version
        ↓
authorize + validate transition
        ↓
UPDATE ... WHERE version = expected
        ↓
version + 1
```

A stale version returns `CONFLICT`.

## Idempotency
Anonymous order submission uses:

```text
store + guest-session hash + idempotency key
```

The server stores request hash + authoritative response so retries return the same order instead of creating another order.
