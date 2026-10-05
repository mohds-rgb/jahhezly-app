# Architecture Decisions

## AD-01 — V1 modular monolith

Use one FastAPI application with clear domain/application/persistence boundaries. This keeps the portfolio system understandable while leaving room for later extraction if real scale requires it.

## AD-02 — SQLite cache on the customer client

Catalog, cart, and sync metadata are durable local concerns. Backend state remains authoritative for commercial facts and order state.

## AD-03 — SYP and bilingual product direction

The owner selected Syrian Pound pricing and Arabic + English as the product languages. Demo catalog content stores English names plus Arabic descriptions as portfolio data.

## AD-04 — Real merchant names, no false endorsement

Paris Market and cham-center are used because the owner authorized use of their names. The repository does not imply endorsement, client contracts, live inventory, or production deployment.

## AD-05 — Multi-branch authorization

A merchant user can hold multiple store memberships. The server resolves capability against the target store for every merchant operation rather than assuming a single default branch.

## AD-06 — Proprietary project license

Original Jahhezly materials are retained under a proprietary license. Third-party packages remain under their own licenses.

## AD-07 — Notification boundary

V1 includes in-app/local notification architecture. Push notification providers are isolated behind a future integration boundary until a real provider is selected and credentials can be supplied securely.

## AD-08 — Medicine delivery removed from scope

The earlier healthcare/pharmacy direction was an owner correction. Jahhezly is a general retail product. Delivery and regulated-goods workflows remain outside V1.
