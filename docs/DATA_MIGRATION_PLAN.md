# Data Migration Plan

## Migration chain

```text
0001 initial schema
   ↓
0002 store location context
   ↓
0003 product localization
   ↓
0004 optional customer contact phone
```

## 0001 — Initial schema

Introduces merchant organizations, stores, staff identities/memberships, catalog, prices, availability, orders, order items, idempotency records, and audit events.

## 0002 — Store context

Adds `city`, `district`, and `branch_code` to stores so a multi-branch retail scenario can be represented without overloading the merchant organization record.

## 0003 — Product localization

Adds Arabic name, description, and category fields while keeping the canonical English fields for API compatibility.

## 0004 — Customer contact phone

Adds nullable `orders.customer_phone` for the contact information needed by the pickup workflow. The field is intentionally nullable to avoid forcing collection of personal data when it is not required by the chosen client flow.

## Safety properties

Each migration is versioned and reversible in the development schema. The current preparation environment exercised:

```text
upgrade head
→ downgrade to 0003
→ upgrade head
```

No mobile migration uses destructive database reset. The mobile client currently uses local schema version `4`, which remains distinct from backend Alembic migration version `0004`.
