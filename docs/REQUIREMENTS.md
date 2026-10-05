# Requirements Traceability

| ID | Priority | Requirement | Implementation | Evidence | Status |
|---|---|---|---|---|---|
| PROD-001 | P1 | Customer browses selected store catalog | `backend/app/api/routes/public.py`, Flutter catalog | backend tests | IMPLEMENTED |
| PROD-002 | P1 | Customer builds a cart/list | `apps/mobile/lib/data/local/local_database.dart` | source inspection | IMPLEMENTED |
| CAT-001 | P0 | Authoritative current price server-side | `backend/app/services/catalog.py` | catalog tests | TESTED |
| CAT-002 | P0 | Historical accepted price preserved | `backend/app/services/orders.py` | order tests | TESTED |
| CAT-003 | P1 | Availability explicit | `ProductAvailability` | catalog tests | TESTED |
| OFF-001 | P1 | Cached catalog usable offline | local SQLite cache | mobile source; device test pending | IMPLEMENTED / UNVERIFIED |
| OFF-002 | P1 | Cart/draft survives offline period | SQLite cart | mobile source; device test pending | IMPLEMENTED / UNVERIFIED |
| OFF-003 | P0 | Offline draft never presented as confirmed order | sync queue states | source inspection | IMPLEMENTED |
| ORD-001 | P1 | Customer can submit order | POST `/v1/orders` | API tests | TESTED |
| ORD-002 | P0 | Order submission idempotent | `IdempotencyRecord` | API tests | TESTED |
| ORD-003 | P0 | Server validates price/availability | `submit_order()` | API tests | TESTED |
| ORD-004..007 | P1 | Merchant progresses order | merchant transition routes | transition tests | TESTED |
| AUTH-001 | P0 | Merchant access server-authorized | JWT + membership | auth tests | TESTED |
| AUTH-002 | P0 | Tenant/store isolation | `require_capability()` | cross-store tests | TESTED |
| SEC-001 | P0 | No production secret in client | environment configuration | validator scan | VERIFIED |
| DATA-001 | P0 | Historical order facts reconstructable | order item snapshots | API/order tests | TESTED |
| MIG-001 | P0 | Versioned recoverable local schema | SQLite 4-version migration + Alembic 0001–0004 | migration checks | TESTED |
| WAP-001 | P1 | WhatsApp-assisted communication | adapter | source + unit test | IMPLEMENTED / UNIT TESTED |
| WAP-002 | P0 | WhatsApp not delivery evidence | adapter boundary | architecture docs | VERIFIED DESIGN |
| UX-001 | P1 | Offline/stale states visible | cached catalog banner | source inspection | IMPLEMENTED |
| AUD-001 | P1 | Sensitive transitions auditable | `AuditEvent` | API tests/source | TESTED |

| DATA-002 | P1 | Customer pickup contact phone is persisted only for order/contact needs | `orders.customer_phone`, request validation | API tests | TESTED |
| NOTIF-001 | P1 | Order status changes have a customer notification surface | order status UI + notification boundary | source inspection | IMPLEMENTED / PROVIDER NOT VERIFIED |
