# Portfolio Demo Scenario

The repository includes a deterministic, portfolio-safe demo seed. Product prices and descriptions are illustrative and must not be treated as live store data.

## Scenario A — Paris Market

1. Seed the demo data.
2. Select **Paris Market — Basra**.
3. Browse the grocery and household catalog.
4. Disconnect the network after catalog synchronization.
5. Continue browsing from the local cache and build a cart.
6. Reconnect and submit the order.
7. Merchant accepts → prepares → marks ready → collects.
8. Customer reads the authoritative order status.

## Scenario B — cham-center

1. Select one of the four `cham-center` demo branches.
2. Verify that merchant access is scoped to the selected branch membership.
3. Update a product price from the merchant API.
4. Refresh the customer catalog.

## Price conflict

Change a product price after the customer has cached the catalog but before submission.

Expected: `409 PRICE_CHANGED`; no order uses the stale commercial value.

## Duplicate request

Repeat the same order submission with the same idempotency key.

Expected: one business order and the same authoritative response.

## Merchant concurrency

Two merchant clients attempt to advance the same order using the same old version.

Expected: one transition succeeds and the stale request receives `409 CONFLICT`.
