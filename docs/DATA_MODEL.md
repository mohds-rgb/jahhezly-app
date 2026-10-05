# Data Model

## Ownership hierarchy

```text
MerchantOrganization
    ↓
Store / Branch
    ↓
Product
    ├── ProductPrice (history)
    └── ProductAvailability

CustomerSession
    ↓
Order
    └── OrderItem (historical snapshots)
```

## Customer contact

`orders.customer_phone` is an optional contact field for pickup communication. It is classified as sensitive personal data and must not be copied into analytics or public demo data.

## Price integrity

Prices are time-aware records. An accepted order stores `unit_price_snapshot`, `currency_snapshot`, and `line_total_snapshot`; today's catalog cannot rewrite the historical commercial facts of an earlier order.

## Order integrity

Order transitions are constrained by the domain state machine and guarded by expected version checks for merchant operations and customer cancellation. Idempotency records bind a request fingerprint to the authoritative response so a retry cannot create a second business order.

## Demo data

`data/demo/` is illustrative portfolio data. It contains no live store inventory, real customer phone numbers, secrets, or production credentials.
