# Privacy Specification

| Data | Classification | Where stored |
|---|---|---|
| Product name | PUBLIC | Catalog / cache |
| Public catalog price | PUBLIC | Catalog / cache |
| Staff membership | CONFIDENTIAL | Backend |
| Customer order | CONFIDENTIAL | Backend + customer local order context where applicable |
| Customer phone | SENSITIVE | Backend order contact field; not included in public demo data |
| Guest session identifier | SENSITIVE | Device local metadata; server stores only a one-way hash |
| Authentication secrets | CRITICAL | Runtime environment / secret manager outside repository |

V1 does not persist a full customer profile, location history, contacts, payment card data, or unnecessary device identifiers.

Guest order ownership uses a one-way server hash of an opaque local session identifier.

The mobile cache is store-scoped so a branch switch cannot expose another branch's cached catalog or cart data through the normal UI path.

Exact retention is an owner/legal decision; the repository uses a 12-month portfolio design default only.
