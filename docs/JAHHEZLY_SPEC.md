# Jahhezly — MASTER ENGINEERING, PRODUCT, SECURITY, DATA-MIGRATION & DELIVERY SPECIFICATION

## Version 1.0 — MASTER — Offline-First Click & Collect, Daily Catalog, Order Preparation & WhatsApp-Assisted Pickup

> **Product:** Jahhezly  
> **Product Type:** Digital pre-order and store-preparation system for Click & Collect  
> **Primary Value:** Let customers prepare a shopping list before visiting the store, allow the store to prepare the order, and minimize waiting time at pickup.  
> **Primary Interaction Model:** Lightweight catalog → cart/list → order submission → store preparation → pickup.  
> **Offline Principle:** Catalog browsing, cached data access, cart construction, and draft preparation MUST remain useful under weak or temporarily unavailable connectivity.  
> **Communication Principle:** WhatsApp MAY be used as a communication/hand-off surface, but MUST NOT become the authoritative source of order truth.  
> **V1 Payment Boundary:** No in-app payment processing unless explicitly approved by the owner. Payment is assumed to occur at the physical store during pickup; this is an implementation assumption, not a legal or accounting decision.  
> **Initial Rollout Context:** The owner described the product in relation to two large stores. The exact merchant identities, branches, countries, currencies, and rollout structure remain owner decisions.  
> **Canonical Status:** This document is the canonical execution contract for the implementation agent until superseded by an explicit owner-approved decision recorded in the project control files.

---

# 0. DOCUMENT IDENTITY, MISSION & BOUNDARY

## 0.1 Mission

Jahhezly MUST reduce avoidable waiting and congestion around physical shopping by allowing customers to prepare purchases in advance from a lightweight digital catalog.

The intended customer journey is:

```text
Open Jahhezly
→ choose/store access
→ browse locally available catalog
→ inspect current/last-known prices
→ add required items
→ review quantity and estimated total
→ connect when submission is required
→ submit order
→ receive order reference
→ store reviews and prepares order
→ customer arrives
→ store confirms payment at pickup
→ customer collects prepared order
```

The system MUST optimize for simplicity, low friction, low bandwidth, and resilience under weak connectivity.

## 0.2 Problem Definition

The product exists to address:

```text
peak-time store congestion
+
time spent browsing shelves
+
uncertain daily prices
+
manual repetitive shopping-list preparation
+
store-side preparation inefficiency
```

The system MUST NOT attempt to solve every retail problem in V1.

## 0.3 V1 Product Objective

V1 MUST provide a credible end-to-end Click & Collect workflow:

```text
catalog
→ price
→ availability
→ cart/list
→ order
→ store acceptance
→ preparation
→ ready for pickup
→ pickup completion
```

The V1 experience MUST remain useful even when the network is poor.

## 0.4 Implementation Boundary

The implementation MUST cover:

- customer-facing experience;
- store/merchant operational experience;
- authoritative catalog and price management;
- order lifecycle management;
- local offline-first persistence;
- synchronization and recovery;
- WhatsApp-assisted communication where approved;
- authentication and authorization for merchant operations;
- auditability;
- migration-safe persistence;
- testing;
- release controls;
- documentation;
- delivery evidence.

The implementation MUST NOT silently expand into:

- delivery logistics;
- online payment processing;
- loyalty programs;
- complex promotions;
- full ERP/POS replacement;
- warehouse management;
- route optimization;
- AI recommendation systems;
- marketplace functionality;
- customer social features;
- subscription billing;
- arbitrary WhatsApp automation;
- financial accounting;
- regulated-goods workflows;

unless separately approved.

---

# 1. NORMATIVE LANGUAGE

This specification uses:

| Term | Meaning |
|---|---|
| **MUST / REQUIRED** | Mandatory |
| **MUST NOT / NEVER / PROHIBITED** | Forbidden |
| **SHOULD** | Strong default unless superseded by an explicit ADR and owner decision |
| **MAY** | Optional |
| **P0** | Security, data, integrity, privacy, safety, or release invariant |
| **P1** | Core product requirement |
| **P2** | Quality, operations, maintainability, accessibility, performance |
| **P3** | Enhancement or experimental capability |
| **INVARIANT** | A condition that MUST remain true |

Critical requirements MUST NOT be described using ambiguous language such as:

```text
try to
ideally
probably
maybe
do your best
as needed
```

---

# 2. AUTHORITY, PRECEDENCE & EVIDENCE

## 2.1 Authority Order

When requirements conflict, use:

```text
1. Explicit current owner decisions in docs/DECISIONS.md
2. Explicit current owner state in PROJECT_STATE.md
3. P0 security/privacy/data/integrity/release invariants
4. Canonical schemas, contracts and state machines
5. P1 product requirements
6. P2 operational/quality requirements
7. P3 enhancements
8. Implementation preferences
```

A lower-priority implementation preference MUST NOT weaken a higher-priority requirement.

## 2.2 Evidence Hierarchy

```text
1. Owner-approved decisions
2. This master specification
3. Actual repository/workspace evidence
4. Current official platform/provider documentation
5. Relevant technical standards
6. Engineering inference
```

Version-sensitive provider, SDK, platform, store-distribution, WhatsApp, operating-system, package, pricing, or quota facts MUST be re-verified at implementation time against current official sources.

## 2.3 Anti-Hallucination Contract

The implementation agent MUST NOT claim that any of the following succeeded without actual evidence:

```text
feature implementation
integration
WhatsApp delivery
database migration
build
test
security control
deployment
release
restore
data synchronization
rollback
artifact verification
```

Statuses MUST remain distinct:

```text
PLANNED
IMPLEMENTED
TESTED
VERIFIED
BUILT
RELEASED
MONITORED
```

---

# 3. AGENT ROLE & EXECUTION CONTRACT

The implementation agent acts simultaneously as:

```text
Principal Product Architect
Lead Software Architect
Domain Architect
Security Architect
Data Architect
Mobile Architect
Integration Architect
QA/Automation Architect
DevOps/Release Architect
SRE/Observability Architect
UX/Accessibility Architect
Documentation Architect
```

The agent MUST:

1. inspect the actual repository before modifying it;
2. establish project state;
3. distinguish facts from assumptions;
4. preserve existing valid work;
5. make changes in dependency order;
6. verify claims with evidence;
7. stop at blocking owner decisions when needed;
8. never invent credentials or provider contracts;
9. never fabricate implementation evidence.

---

# 4. OWNER FACTS, ASSUMPTIONS & OPEN DECISIONS

## 4.1 Current Owner Facts

The following facts come directly from the project idea:

- Project name: **Jahhezly**
- The product is a Click & Collect / preorder concept.
- Customers should see available goods and their current prices.
- Customers should be able to prepare a list/order before visiting.
- The store prepares the order.
- The customer comes to pay and collect.
- The product is intended to reduce peak-time congestion and browsing time.
- Offline-first behavior is a critical success factor.
- WhatsApp is an important communication mechanism.
- Simplicity and speed are critical UX requirements.

## 4.2 Engineering Defaults

The following are engineering defaults, not owner facts:

- Flutter is the default mobile technology.
- Local persistence SHOULD use SQLite through a typed abstraction such as Drift or equivalent.
- A modular monolithic backend is preferred for V1.
- A relational datastore such as PostgreSQL is the default backend datastore.
- REST/HTTP is the default API transport.
- Merchant operations SHOULD be available through a role-controlled merchant application or responsive operational surface.
- Customer registration SHOULD NOT be mandatory for basic catalog browsing.
- Online payment SHOULD remain outside V1.
- WhatsApp SHOULD initially be treated as a communication surface rather than the authoritative transaction system.

Any replacement requires a documented architecture decision.

## 4.3 Mandatory Owner Decisions

The implementation agent MUST create `OPEN_QUESTIONS.md` containing at minimum:

| ID | Decision |
|---|---|
| OQ-01 | Target country/market |
| OQ-02 | Currency and regional number/date conventions |
| OQ-03 | Exact two initial merchant/store organizations |
| OQ-04 | Whether each merchant has multiple physical branches |
| OQ-05 | Customer authentication requirement, if any |
| OQ-06 | Merchant/staff authentication mechanism |
| OQ-07 | WhatsApp mode: native deep-link/share in V1 vs official programmable integration |
| OQ-08 | Whether customers may submit orders as guests |
| OQ-09 | Business policy when item availability changes after customer submission |
| OQ-10 | Whether substitutions are allowed |
| OQ-11 | Order expiration / uncollected-order policy |
| OQ-12 | Pickup verification mechanism |
| OQ-13 | Whether the customer stores a phone number inside Jahhezly |
| OQ-14 | Customer notification mechanism beyond WhatsApp |
| OQ-15 | Data retention period |
| OQ-16 | Hosting/deployment region |
| OQ-17 | Tax/invoice requirements |
| OQ-18 | Official brand assets, typography and visual language |
| OQ-19 | Target platforms and minimum supported OS versions |
| OQ-20 | Production launch/distribution strategy |

Do NOT invent answers.

---

# 5. PROJECT CONTROL FILES

The repository MUST contain only control files that have a real purpose.

Recommended initial structure:

```text
PROJECT_STATE.md
OPEN_QUESTIONS.md
ASSUMPTIONS.md
RISK_REGISTER.md
SECURITY_RISK_REGISTER.md

docs/
  JAHHEZLY_SPEC.md
  REQUIREMENTS.md
  DECISIONS.md
  ARCHITECTURE.md
  SECURITY_REFERENCES.md
  UX_SPEC.md
  API_CONTRACT.md
  DATA_MIGRATION_PLAN.md
  RELEASE_PLAN.md
  OPERATIONS_RUNBOOK.md
  PRIVACY_SPEC.md
  INTEGRATION_SPEC.md

DELIVERY_MANIFEST.md
CHANGELOG.md
```

## 5.1 PROJECT_STATE.md

The project state MUST always indicate:

```text
current phase
current gate
last verified change
repository state
known blockers
open owner decisions
implementation status
test status
build status
release status
next safe action
```

---

# 6. PRODUCT SCOPE

## 6.1 V1 In-Scope

### Customer

```text
store selection
catalog browsing
category browsing
product search/filter where justified
product details
current/last-known price visibility
availability visibility
quantity management
cart/list creation
order review
order submission
order reference
order status
WhatsApp-assisted communication
offline catalog access
offline cart/list construction
local order draft persistence
```

### Merchant / Store Staff

```text
authenticated staff access
catalog management
product activation/deactivation
price management
availability management
incoming order queue
order inspection
order acceptance/rejection
order preparation status
ready-for-pickup status
pickup completion
basic operational search
```

### Administrative Controls

Only where necessary for V1:

```text
merchant organization management
branch/store configuration
staff role assignment
audit visibility
configuration of WhatsApp contact information
```

## 6.2 Explicitly Out of Scope for V1

```text
delivery
route planning
courier management
online card/payment processing
wallets
refund workflows
subscription billing
advanced loyalty
dynamic coupon engines
AI recommendations
social functionality
marketplace-to-many-merchants discovery
full POS replacement
warehouse management
accounting
complex procurement
real-time inventory synchronization with external ERP
automated WhatsApp bot conversations
```

---

# 7. ACTORS & AUTHORIZATION

## 7.1 Actors

The V1 model SHOULD contain:

```text
Customer
Store Operator
Store Manager
Merchant Administrator
System
WhatsApp / external communication surface
```

A global Super Admin MAY exist only if operationally necessary.

## 7.2 Customer

Customers MAY browse the catalog without creating a full account.

If customer accounts are introduced:

```text
customer identity
profile
preferences
order ownership
```

MUST be separated from merchant identities.

Customer authorization MUST prevent a customer from accessing another customer's order.

## 7.3 Store Operator

Can:

```text
view authorized incoming orders
accept/reject orders
prepare orders
mark ready
mark collected
```

Cannot:

```text
change global platform policy
access unrelated merchants
modify another merchant's users
view unnecessary platform secrets
```

## 7.4 Store Manager

Can:

```text
manage catalog
manage daily prices
manage availability
manage order operations
manage store-specific settings
view authorized operational analytics
```

## 7.5 Merchant Administrator

Can:

```text
manage organization settings
manage branches
manage authorized staff
manage merchant-level settings
```

## 7.6 Authorization Invariant

The server MUST derive authorization from authenticated identity and authoritative membership data.

The client MUST NOT be trusted for:

```text
tenantId
organizationId
storeId
role
isAdmin
isManager
capabilities
ownership
```

---

# 8. MULTI-TENANCY & ORGANIZATION MODEL

Because the concept is intended to serve more than one store, the architecture MUST support tenant isolation even if the initial deployment contains only two merchants.

Preferred logical structure:

```text
MerchantOrganization
    ↓
Store / Branch
    ↓
Catalog
    ↓
Product
    ↓
Price
    ↓
Availability
```

Customer order ownership:

```text
Customer / Guest Order Session
    ↓
Order
    ↓
Order Items
    ↓
Product/Price snapshots
```

Every merchant-owned resource MUST have an authoritative organization/store ownership boundary.

Cross-tenant access MUST fail closed.

---

# 9. DOMAIN MODEL

## 9.1 Core Aggregates

The domain SHOULD use:

```text
MerchantOrganization
Store
Catalog
Product
ProductPrice
ProductAvailability
Order
OrderItem
CustomerSession
StaffMembership
AuditEvent
```

Potential future aggregates:

```text
Promotion
Substitution
PickupSlot
Payment
Notification
ERPIntegration
```

These future concepts MUST NOT be implemented prematurely.

## 9.2 Product

A Product SHOULD contain:

```text
id
storeId / catalog context
name
description
category
unitLabel
active
image reference where applicable
createdAt
updatedAt
version
```

The canonical product identity MUST be stable.

## 9.3 Price

Price MUST be modeled as a time-aware business fact rather than overwritten blindly.

A price record SHOULD include:

```text
id
productId
amount
currency
effectiveFrom
effectiveTo nullable
status
createdAt
createdBy
version
```

A historical order MUST retain the price used at order acceptance.

## 9.4 Availability

Availability SHOULD be distinct from price.

Minimum conceptual state:

```text
AVAILABLE
UNAVAILABLE
```

Do not infer availability from UI visibility alone.

## 9.5 Order

An Order MUST contain:

```text
id
publicOrderCode
storeId
customer/session reference where applicable
state
submittedAt
acceptedAt
preparingAt
readyAt
collectedAt
cancelledAt
estimated/actual totals where applicable
version
createdAt
updatedAt
```

## 9.6 Order Item

Each order item MUST preserve a historical snapshot sufficient to reconstruct what the customer requested at submission time:

```text
productId
productNameSnapshot
quantity
unitPriceSnapshot
currencySnapshot
lineTotalSnapshot
itemState where applicable
```

Current product data MUST NOT silently rewrite historical order information.

---

# 10. SOURCE OF TRUTH INVARIANT

The system MUST use:

```text
authoritative backend state
>
client state
>
local cache
```

for server-owned business truth.

Local cache MUST NOT override server-owned:

```text
final price
availability
order state
merchant identity
authorization
pickup status
```

The local database is authoritative only for explicitly local concerns such as:

```text
cached catalog data
user preferences
unsent drafts
local synchronization metadata
```

---

# 11. CATALOG & DAILY PRICE ARCHITECTURE

## 11.1 Catalog Principle

The catalog SHOULD be lightweight enough to load and remain useful under weak connectivity.

The local client SHOULD store:

```text
catalog metadata
product records
category information
last-known prices
availability snapshot
catalog version
last synchronized timestamp
```

## 11.2 Freshness

Every cached catalog MUST retain:

```text
lastSyncedAt
catalogVersion
sourceVersion
```

The UI MUST clearly differentiate:

```text
current/recently synchronized
cached
stale
unavailable
```

A stale local price MUST NEVER be presented as guaranteed current.

## 11.3 Order-Time Validation

When an order is submitted:

```text
client cart
→ backend validates product identity
→ backend validates availability
→ backend obtains authoritative current price
→ backend calculates accepted order values
→ backend stores immutable snapshots
```

The client MUST NOT be authoritative for final commercial values.

## 11.4 Price Change Invariant

If a product's current price differs from the customer's cached price:

```text
submission MUST NOT silently accept the stale price
```

The API SHOULD return a structured conflict such as:

```text
PRICE_CHANGED
```

The customer MUST be shown the updated value and must explicitly continue where business policy requires confirmation.

---

# 12. ORDER STATE MACHINE

## 12.1 Canonical States

V1 order states:

```text
DRAFT
PENDING_SUBMISSION
SUBMITTED
ACCEPTED
PREPARING
READY_FOR_PICKUP
COLLECTED
REJECTED
CANCELLED
```

`DRAFT` and `PENDING_SUBMISSION` MAY exist locally before the backend owns the order.

## 12.2 Allowed Server Transitions

```text
SUBMITTED
  → ACCEPTED
  → REJECTED
  → CANCELLED

ACCEPTED
  → PREPARING
  → CANCELLED

PREPARING
  → READY_FOR_PICKUP
  → CANCELLED

READY_FOR_PICKUP
  → COLLECTED
  → CANCELLED where business policy allows
```

Terminal states:

```text
COLLECTED
REJECTED
CANCELLED
```

Terminal states MUST NOT be silently reactivated.

## 12.3 Transition Requirements

Every transition MUST validate:

```text
current state
actor identity
actor capability
ownership/store
preconditions
version/concurrency
```

Each successful transition SHOULD emit an audit event.

Unknown transitions MUST be rejected.

## 12.4 Pickup Invariant

An order MUST NOT become `COLLECTED` merely because:

```text
customer opened a screen
WhatsApp opened
a client request was sent
the order existed
```

A store-authorized action MUST be the source of the pickup completion event.

Payment itself is outside the application's payment processing boundary unless separately approved.

---

# 13. OFFLINE-FIRST ARCHITECTURE

Offline-first is a product requirement, not a marketing label.

## 13.1 Safe Offline Operations

The customer MUST be able to perform, where previously synchronized data exists:

```text
open app
browse cached catalog
browse cached categories
view cached prices with freshness indicators
build/edit cart
change quantities
save shopping draft
review local draft
```

## 13.2 Network-Required Operations

The following remain authoritative network operations:

```text
final order submission
authoritative price validation
authoritative availability validation
order status synchronization
merchant operations
```

## 13.3 Offline Order Submission

A customer MAY press "Submit" while offline.

The application MUST NOT falsely display:

```text
Order submitted
```

unless a backend acknowledgement exists.

Instead:

```text
saved locally
→ queued for submission
→ waiting for connection
```

must remain distinct from:

```text
submitted
```

## 13.4 Sync Queue

If offline submission is supported, each queued mutation MUST contain:

```text
localOperationId
idempotencyKey
createdAt
operationType
payloadVersion
retryCount
status
lastAttemptAt
lastFailureCode
```

The queue MUST survive:

```text
app restart
device restart
temporary network loss
process termination
```

## 13.5 Synchronization Rules

The synchronization system MUST:

```text
retry safely
avoid duplicate orders
use the same idempotency key
reconcile authoritative state
surface conflicts
avoid silent destructive merges
```

---

# 14. LOCAL STORAGE ARCHITECTURE

Default implementation:

```text
Flutter
+
SQLite
+
typed persistence abstraction such as Drift
```

The exact library MAY change with an ADR.

## 14.1 Local Storage Categories

### Cache

```text
products
categories
prices
availability
catalog metadata
```

### Durable User Data

```text
draft cart
local preferences
sync metadata
```

### Potentially Sensitive

```text
customer identity/session information
order details
phone number if stored
```

Sensitive local data SHOULD be minimized and protected appropriately.

## 14.2 Local Schema Versioning

Every local schema MUST define:

```text
schemaVersion
migrationVersion
fromVersion
toVersion
migration steps
preconditions
postconditions
verification
```

Migrations MUST be:

```text
versioned
deterministic
idempotent
resumable
non-destructive
testable
interruption-safe
```

Normal application updates MUST NOT call:

```text
clear()
reset()
deleteEverything()
```

as a migration strategy.

---

# 15. IDEMPOTENCY, REPLAY & CONCURRENCY

Order submission is a critical duplicate-sensitive operation.

## 15.1 Submission Identity

Each submission MUST use an idempotency key.

Recommended request context:

```text
idempotencyKey
requestHash
customer/session identity
storeId
aggregateId where known
requestedAt
clientVersion
correlationId
```

## 15.2 Retry Rule

When:

```text
request sent
→ server commits
→ response lost
```

the client MUST:

```text
retry the SAME idempotency key
→ retrieve authoritative result
→ reconcile local state
```

It MUST NOT create a second order.

## 15.3 Concurrency Examples

The test suite MUST verify:

```text
same order submitted twice concurrently
→ exactly one business order

two merchant operators update one order
→ version conflict is handled safely

customer submits using stale price
→ authoritative conflict is returned

merchant attempts invalid state transition
→ rejected

old client repeats a previous command
→ no duplicate side effect
```

---

# 16. API / CONTRACT SPECIFICATION

Default transport:

```text
HTTPS REST API
versioned under /v1
```

Every endpoint MUST document:

```text
path
method
authentication
authorization
request schema
query parameters
headers
validation
response schema
error codes
idempotency
retryability
pagination where applicable
audit behavior
side effects
privacy classification
compatibility behavior
tests
```

## 16.1 Customer API Surface

Conceptually:

```text
GET  /v1/stores
GET  /v1/stores/{storeId}/catalog
GET  /v1/stores/{storeId}/categories
GET  /v1/orders/{orderId}
POST /v1/orders
POST /v1/orders/{orderId}/cancel
```

Exact endpoint design MAY change after architecture review.

## 16.2 Merchant API Surface

Conceptually:

```text
GET   /v1/merchant/orders
GET   /v1/merchant/orders/{orderId}
POST  /v1/merchant/orders/{orderId}/accept
POST  /v1/merchant/orders/{orderId}/reject
POST  /v1/merchant/orders/{orderId}/start-preparing
POST  /v1/merchant/orders/{orderId}/ready
POST  /v1/merchant/orders/{orderId}/collect
GET   /v1/merchant/catalog
POST  /v1/merchant/catalog/products
PATCH /v1/merchant/catalog/products/{productId}
POST  /v1/merchant/catalog/products/{productId}/price
POST  /v1/merchant/catalog/products/{productId}/availability
```

Every actual route MUST be documented before being treated as implemented.

---

# 17. ERROR MODEL

The system MUST expose stable machine-readable codes.

Minimum shared codes:

```text
UNAUTHORIZED
FORBIDDEN
RESOURCE_NOT_FOUND
INVALID_REQUEST
RATE_LIMITED
CONFLICT
SERVICE_UNAVAILABLE
INTEGRATION_UNAVAILABLE
MIGRATION_FAILED
UPDATE_REQUIRED
UPDATE_AVAILABLE
STALE_DATA
PRICE_CHANGED
PRODUCT_UNAVAILABLE
ORDER_NOT_SUBMITTABLE
INVALID_STATE_TRANSITION
DUPLICATE_REQUEST
SYNC_PENDING
```

Clients MUST map codes to localized messages.

Raw server exceptions MUST NOT be shown to customers.

---

# 18. WHATSAPP INTEGRATION BOUNDARY

WhatsApp is explicitly relevant to Jahhezly but MUST be isolated from the core domain.

## 18.1 V1 Preferred Approach

The default V1 integration SHOULD be:

```text
Jahhezly creates validated order/message content
→ user explicitly chooses WhatsApp
→ operating system opens WhatsApp or the supported share/deep-link surface
→ user confirms/sends through WhatsApp
```

This avoids making the entire customer ordering experience dependent on permanent connectivity or a complex programmable-messaging backend.

The exact deep-link/share implementation MUST be verified against current official platform/provider documentation at implementation time.

## 18.2 WhatsApp Is Not Source of Truth

Jahhezly MUST NOT treat:

```text
WhatsApp opening
message composer opening
user pressing share
```

as proof that:

```text
message delivered
message read
store received
store accepted order
```

Those states require actual evidence.

## 18.3 Message Payload

A generated WhatsApp message MAY include:

```text
Jahhezly
store name
human-readable order code
items
quantities
order summary
pickup instruction
customer notes where approved
```

It MUST NOT include unnecessary sensitive information.

## 18.4 WhatsApp Failure

If WhatsApp is unavailable:

```text
the core order MUST remain valid
```

The business state MUST NOT be rolled back merely because communication through WhatsApp failed.

The customer SHOULD be offered the order reference and an alternative contact mechanism.

## 18.5 Official Programmable WhatsApp Integration

An official API-based integration is:

```text
FUTURE / OWNER DECISION REQUIRED
```

If later enabled, it MUST introduce:

```text
provider credentials
provider verification
provider-specific rate limits
template/business rules where applicable
webhook verification
provider outage behavior
message idempotency
delivery evidence
provider-version tracking
cost governance
privacy/data-sharing analysis
```

No production provider credentials may be invented.

---

# 19. CUSTOMER EXPERIENCE

## 19.1 UX Principles

Jahhezly SHOULD feel:

```text
fast
simple
predictable
quiet
lightweight
obvious
mobile-first
Arabic-friendly where Arabic is the chosen target language
```

The interface MUST not overload the user with configuration or unnecessary workflow steps.

## 19.2 Core Surfaces

Minimum customer surfaces:

```text
Store Selection
Home/Catalog
Category
Product Details
Cart
Order Review
Submission Result
Order Status
Order History / Local Orders where applicable
Offline State
Settings
```

## 19.3 Every Critical Flow Must Define

```text
loading
empty
success
failure
retry
offline
timeout
stale data
conflict
duplicate action
permission/session issues where applicable
maintenance
```

---

# 20. MERCHANT EXPERIENCE

The merchant surface MUST prioritize operational speed over visual complexity.

Minimum screens:

```text
Merchant Login
Store Dashboard
Incoming Orders
Order Details
Preparation Workflow
Ready-for-Pickup Queue
Collected Orders
Catalog
Product Editor
Price Management
Availability Management
Staff/Settings where authorized
Audit/Activity where necessary
```

## 20.1 Incoming Order Queue

The queue SHOULD prioritize:

```text
newest actionable orders
current status
order age
store/branch
item count
```

The system SHOULD support clear operational scanning without excessive navigation.

## 20.2 Merchant Race Safety

Two operators opening the same order MUST NOT be able to produce contradictory final states through stale UI.

Optimistic concurrency or equivalent state/version validation MUST be used.

---

# 21. DATA INTEGRITY INVARIANTS

The following are P0:

```text
INVARIANT-01
A customer-visible cached price is never treated as authoritative at final submission.

INVARIANT-02
An order item preserves the price/name facts applicable at order acceptance.

INVARIANT-03
A store operator cannot mutate another merchant's order.

INVARIANT-04
An invalid order state transition is always rejected.

INVARIANT-05
Repeated submission with the same idempotency key cannot create duplicate business effects.

INVARIANT-06
A local draft is never represented as a confirmed backend order.

INVARIANT-07
Opening or composing a WhatsApp message is never treated as proof of delivery.

INVARIANT-08
A collected order cannot silently return to preparing.

INVARIANT-09
Historical order facts cannot be rewritten merely because today's catalog changed.

INVARIANT-10
Normal application updates preserve durable local data.

INVARIANT-11
No real secret is embedded in client source or release artifacts.

INVARIANT-12
Sensitive personal data is not sent to analytics merely because it exists.

INVARIANT-13
Cache data never overrides backend authorization or business state.

INVARIANT-14
Merchant access is tenant/store scoped.

INVARIANT-15
Payment processing is not silently introduced into V1.
```

---

# 22. SECURITY ARCHITECTURE

## 22.1 Threat Priorities

The most valuable assets are:

```text
merchant credentials
customer order data
merchant catalog/prices
merchant authorization
order state
business history
provider credentials
session tokens
```

## 22.2 Primary Threats

The project MUST evaluate:

```text
broken access control
tenant breakout
IDOR
privilege escalation
stolen merchant session
mass assignment
malicious order creation
duplicate order submission
replay attacks
price tampering
availability manipulation
order state tampering
API enumeration
rate abuse
credential leakage
secret extraction from client
supply-chain compromise
data exposure
unsafe deep-link handling
```

## 22.3 Customer Abuse

Public or semi-public order creation MAY be abused for:

```text
spam
order flooding
resource exhaustion
fake demand
merchant harassment
```

Rate controls SHOULD consider:

```text
IP
anonymous session
authenticated identity where available
device/session characteristics
store
endpoint
operation
```

Rate limiting MUST NOT replace authorization.

## 22.4 Secret Management

Absolute rule:

```text
No real secret may be hardcoded.
```

Never include real credentials in:

```text
Flutter source
assets
APK/AAB
public configuration
Git
logs
screenshots
documentation
demo artifacts
```

`.env` files MUST NOT be treated as secure production secret vaults.

---

# 23. INPUT VALIDATION

All inputs MUST define:

```text
type
required/optional
maximum length
allowed characters
range
enum
normalization
semantic rules
```

Examples requiring validation:

```text
product name
description
price
currency
quantity
customer note
order identifier
store identifier
search query
staff input
WhatsApp message content
```

The server MUST revalidate all trust-sensitive input.

The client MUST NOT be considered a validation boundary.

---

# 24. PRIVACY & DATA CLASSIFICATION

## 24.1 Classification

Use:

```text
PUBLIC
INTERNAL
CONFIDENTIAL
SENSITIVE
CRITICAL
```

Example classification:

| Data | Classification |
|---|---|
| Published product name | PUBLIC |
| Public catalog price | PUBLIC |
| Merchant internal notes | INTERNAL |
| Staff membership | CONFIDENTIAL |
| Customer order details | CONFIDENTIAL |
| Customer phone, if stored | SENSITIVE |
| Authentication secrets | CRITICAL |

## 24.2 Data Minimization

Do not collect:

```text
full customer profile
location history
contacts
unnecessary device data
payment card information
```

unless a concrete V1 requirement demands it.

## 24.3 Analytics

Analytics MUST NOT contain:

```text
passwords
access tokens
provider secrets
raw WhatsApp message bodies
unnecessary personal data
```

Preferred events:

```text
catalog_opened
product_viewed
cart_created
order_submitted
order_accepted
order_ready
order_collected
sync_failed
sync_recovered
```

Events SHOULD use non-sensitive identifiers or aggregation.

---

# 25. DATA RETENTION

Every authoritative entity MUST define:

```text
creation
active lifetime
retention
archival where applicable
deletion
anonymization where applicable
audit retention
migration impact
```

Order history MUST NOT be deleted merely to simplify the current UI.

Exact legal/accounting retention periods remain owner/legal decisions.

---

# 26. OBSERVABILITY

Where backend/runtime infrastructure exists, structured logs SHOULD include:

```text
requestId
correlationId
actorId where available
tenantId where authorized
storeId
operation
result
latency
errorCode
version
```

Never log:

```text
passwords
tokens
provider credentials
sensitive personal information
full unnecessary order notes
```

## 26.1 Operational Metrics

Track at minimum:

```text
catalog sync success/failure
catalog freshness
order submission success rate
order submission conflict rate
duplicate submission prevention
order processing time
ready-for-pickup age
pickup completion rate
API latency
error rates
sync queue backlog
```

Golden signals:

```text
latency
traffic
errors
saturation
```

---

# 27. PERFORMANCE BUDGETS

Performance targets are engineering goals, not guarantees.

Suggested initial targets:

| Flow | Engineering Target |
|---|---:|
| Cached app/catalog opening | P95 ≤ 2.0s |
| Cached category navigation | P95 ≤ 500ms |
| Cart interaction | P95 ≤ 150ms perceived response |
| Catalog refresh under normal network | P95 ≤ 3s |
| Standard order API round trip | P95 ≤ 2.5s |
| Merchant order queue load | P95 ≤ 2.5s |

The actual target MUST be validated on representative devices and realistic network conditions.

Offline-first performance SHOULD be measured from local storage rather than simulated network responses.

---

# 28. COST GOVERNANCE

V1 MUST remain operationally lightweight.

The architecture MUST NOT introduce:

```text
Kafka
Redis cluster
microservice fleet
complex event bus
multiple databases
search cluster
```

without demonstrated need.

Preferred V1 architecture:

```text
one backend application
one primary relational datastore
local client database
optional object storage only if product assets require it
```

Scale-out decisions MUST be based on:

```text
traffic
latency
database contention
storage growth
operational complexity
cost
```

Third-party usage and billing MUST be verified against current provider terms before production commitments.

---

# 29. ARCHITECTURE DECISION DEFAULT

## AD-01 — Default V1 Architecture

Recommended baseline:

```text
Customer Mobile App
        |
        | HTTPS
        v
Modular Monolith API
        |
        v
Relational Database
```

Customer local layer:

```text
Flutter UI
→ application/use-case layer
→ repository abstraction
→ local SQLite
→ synchronization layer
→ API client
```

Merchant surface:

```text
Merchant UI
→ application/use-case layer
→ API
→ authorization
→ relational datastore
```

WhatsApp:

```text
Jahhezly communication adapter
→ user-controlled WhatsApp opening/share
```

The architecture MUST NOT depend on WhatsApp for transactional correctness.

---

# 30. PROJECT STRUCTURE

A practical repository MAY use:

```text
/
├── apps/
│   ├── customer/
│   └── merchant/
│
├── packages/
│   ├── domain/
│   ├── data/
│   ├── ui/
│   ├── localization/
│   ├── networking/
│   └── offline_sync/
│
├── backend/
│   ├── api/
│   ├── application/
│   ├── domain/
│   ├── infrastructure/
│   ├── migrations/
│   └── tests/
│
├── docs/
├── scripts/
├── test/
└── CI configuration
```

The agent MAY simplify this when the actual repository is smaller, but SHOULD maintain clean boundaries between:

```text
presentation
application/use-cases
domain
persistence
integration
```

---

# 31. DESIGN SYSTEM

Jahhezly SHOULD use a small reusable design system.

Define:

```text
colors
typography
spacing
radii
buttons
inputs
cards
lists
badges
dialogs
navigation
loading states
error states
empty states
offline indicators
```

The visual direction SHOULD reflect:

```text
retail utility
trust
speed
clarity
simplicity
low cognitive load
```

Do not add decorative complexity that makes product discovery slower.

Official owner-provided brand assets, when available, take precedence.

---

# 32. LOCALIZATION & ACCESSIBILITY

## 32.1 Localization

Because the original concept is written for an Arabic-oriented audience, Arabic-first presentation is a reasonable product default.

However, exact language policy remains owner-controlled.

The architecture MUST support:

```text
RTL
LTR
localized dates
localized numbers
localized currency
localized errors
localized statuses
```

Hardcoded user-facing strings SHOULD be prohibited.

## 32.2 Accessibility

Critical flows MUST support:

```text
readable typography
dynamic text sizing
touch targets
screen-reader semantics
meaningful labels
non-color-only status communication
adequate contrast
logical navigation
```

---

# 33. PRODUCT SURFACE INVENTORY

Every implemented surface MUST be documented using:

| Surface | Actor | Purpose | Data Source | Permissions | Offline |
|---|---|---|---|---|---|
| Catalog | Customer | Browse products | Local cache/backend | Public/selected store | Yes |
| Product Detail | Customer | Inspect product | Local cache/backend | Public/selected store | Yes |
| Cart | Customer | Prepare purchase | Local DB | Local | Yes |
| Order Review | Customer | Confirm submission | Local + backend validation | Customer/session | Partially |
| Order Status | Customer | Track order | Backend/local cache | Owner/session | Read-only cached |
| Incoming Orders | Merchant | Process orders | Backend | Merchant role | No |
| Preparation | Merchant | Advance order state | Backend | Operator | No |
| Catalog Management | Manager | Maintain products | Backend | Manager | No |
| Price Management | Manager | Maintain current prices | Backend | Manager | No |
| Availability | Manager | Control store availability | Backend | Manager | No |

---

# 34. SUPPORT & OPERATIONS

V1 MAY use a simple support model based on:

```text
store contact
WhatsApp contact
order reference
manual support escalation
```

A full ticketing system is not required unless approved.

Support staff MUST receive least-privilege access.

Customer communications MUST NOT expose unnecessary data.

---

# 35. AUDITABILITY

High-value events MUST create immutable or append-only audit records where practical.

At minimum:

```text
catalog price changed
availability changed
order submitted
order accepted
order rejected
order started
order marked ready
order collected
staff role changed
merchant settings changed
security-sensitive configuration changed
```

An audit record SHOULD contain:

```text
eventId
timestamp
actorId
tenant/store context
aggregateId
action
before/after summary where appropriate
correlationId
```

Secrets MUST NOT be included.

---

# 36. THREAT MODEL

| Asset | Threat | Impact | Control |
|---|---|---|---|
| Merchant account | Credential theft | High | Strong auth/session controls |
| Order state | Client tampering | High | Server-side authorization/state machine |
| Daily prices | Client manipulation | High | Server-authoritative pricing |
| Catalog | Unauthorized editing | High | Role/store authorization |
| Orders | Duplicate submission | High | Idempotency |
| Customer data | Unauthorized access | High | Object-level authorization |
| WhatsApp flow | False delivery assumption | Medium/High | Explicit evidence states |
| Local cache | Stale data | Medium | Freshness metadata |
| API | Order spam | Medium/High | Rate limiting and abuse controls |
| Secrets | Client extraction | Critical | Server-side secret storage |

---

# 37. INCIDENT RESPONSE

The implementation MUST document response for:

```text
merchant account takeover
tenant data exposure
price manipulation
order duplication
catalog corruption
migration failure
database outage
API outage
provider/WhatsApp issue
credential compromise
malicious order flooding
```

Incident procedures MUST preserve:

```text
timestamps
logs
request identifiers
relevant audit records
deployment version
migration version
```

Evidence MUST NOT be destroyed during remediation.

---

# 38. MIGRATION & UPDATE MASTER INVARIANT

A new release is an upgrade of the existing installed system, not a clean reinstall.

The project MUST target:

```text
zero intentional data loss
+
zero intentional destructive reset
+
controlled local schema evolution
+
controlled backend schema evolution
+
backward-compatible API changes where feasible
+
recoverable migrations
```

## 38.1 Mobile Update Preservation

Where applicable, preserve:

```text
application identity
local catalog cache
draft carts
queued synchronization state
preferences
customer local data
valid session state
```

unless the owner has explicitly approved a destructive change.

Unexpected destructive data loss is a P0 release failure.

---

# 39. BACKEND MIGRATIONS

Backend migrations MUST support:

```text
version tracking
compatibility windows
backfills where needed
progress tracking
idempotency
paging
verification
partial failure recovery
old-client compatibility
```

No unbounded database-wide work MUST occur inside an ordinary request path.

Migration interruption MUST be tested using:

```text
process kill
timeout
partial batch
network interruption
duplicate execution
concurrent deployment
```

---

# 40. BACKWARD COMPATIBILITY

For every significant release evaluate:

| Client / Backend | Compatibility |
|---|---|
| N-2 client | assess |
| N-1 client | assess |
| N client | assess |
| N client with existing cloud data | assess |
| N+1 client with legacy data | assess |

The actual supported compatibility window MUST be documented in `RELEASE_PLAN.md`.

---

# 41. RELEASE SAFETY

Every releasable version MUST identify:

```text
version name
build/version code
Git commit
build timestamp
API version
schema version
migration version
platform target
release channel
```

A release artifact MUST NOT be marked verified without actual evidence.

---

# 42. MOBILE RELEASE REQUIREMENTS

Where mobile distribution applies:

```text
application identifier
version
build number
minimum OS
target platform
permissions
network security
signing configuration
artifact integrity
store requirements
```

Private signing keys and passwords MUST remain outside ordinary project archives.

---

# 43. CI/CD & SUPPLY-CHAIN SECURITY

CI SHOULD include:

```text
dependency validation
secret scanning
lint/static analysis
unit tests
domain tests
integration tests
security tests
migration tests
build verification
artifact generation
artifact hash generation
```

Production credentials MUST NOT be stored in source control.

Third-party dependencies MUST be reviewed when they enter security-sensitive paths.

---

# 44. TEST PYRAMID

The project MUST implement applicable layers:

```text
unit
domain
repository
API
authorization
security
database/integrity
concurrency
migration
offline synchronization
UI
localization
accessibility
integration
build/release
```

## 44.1 Critical Product Scenarios

Tests MUST verify:

```text
catalog available offline
cached catalog shown correctly
stale price visibly identified
cart persists after restart
offline draft persists
reconnection does not duplicate order
price change is detected
unavailable item is handled explicitly
merchant accepts order
merchant advances preparation
merchant marks ready
authorized staff completes pickup
unauthorized staff cannot modify order
terminal order cannot be reopened
```

---

# 45. OFFLINE & MIGRATION TEST MATRIX

| Scenario | Expected |
|---|---|
| Open app with no network | Cached catalog available |
| No cached catalog | Clear unavailable state |
| Network drops while browsing | Continue from local cache |
| Network drops while editing cart | Cart preserved |
| Restart after offline cart creation | Cart preserved |
| Queue order while offline | Clearly marked pending |
| Reconnect after queued order | One authoritative order |
| Server response lost after commit | Retry same idempotency key |
| App killed during sync | Safe recovery |
| Local migration interrupted | Safe resume/recovery |
| New version installed | Durable local data preserved |

---

# 46. LOAD & CONCURRENCY TESTING

The project MUST test real bottlenecks rather than inventing large-scale infrastructure.

Minimum scenarios:

```text
many customers loading public catalog
many customers submitting orders around peak time
many merchant operators processing orders
duplicate submission bursts
same order opened by multiple operators
rapid price changes during order submissions
catalog synchronization during peak traffic
```

Load test documentation MUST contain:

```text
environment
load level
duration
threshold
actual result
bottleneck
remediation
```

---

# 47. PHASED EXECUTION PLAN

## Phase 0 — Discovery & Control

Deliver:

```text
repository audit
PROJECT_STATE.md
ASSUMPTIONS.md
OPEN_QUESTIONS.md
initial threat model
architecture baseline
requirements baseline
```

Gate:

```text
G0 Discovery
```

## Phase 1 — Foundation

Implement:

```text
project structure
authentication foundation for merchant roles
tenant/store isolation
shared models
local persistence foundation
API foundation
error model
logging foundation
```

Gate:

```text
G1 Foundation
```

## Phase 2 — Catalog Vertical Slice

Implement end-to-end:

```text
merchant product management
price management
availability
backend catalog
API
local cache
customer catalog UI
offline reads
tests
```

Gate:

```text
G2 Catalog/Data Integrity
```

## Phase 3 — Cart & Order Vertical Slice

Implement:

```text
cart
order creation
server validation
price snapshotting
idempotency
state machine
merchant incoming orders
```

Gate:

```text
G3 Order/Concurrency Integrity
```

## Phase 4 — Preparation & Pickup

Implement:

```text
accept
prepare
ready
collect
merchant operational views
audit trail
customer order status
```

Gate:

```text
G4 Operational Workflow Integrity
```

## Phase 5 — Offline Synchronization & WhatsApp

Implement:

```text
offline drafts
queued submission
recovery
sync conflicts
WhatsApp-assisted communication
integration boundary
failure handling
```

Gate:

```text
G5 Offline/Integration Integrity
```

## Phase 6 — Hardening

Implement and verify:

```text
security
privacy
accessibility
localization
performance
abuse controls
observability
migration tests
release controls
```

Gate:

```text
G6 Hardening
```

## Phase 7 — Release

Produce:

```text
real build
verified artifact
hashes
release manifest
migration evidence
test evidence
known limitations
rollback/recovery notes
```

Gate:

```text
G7 Release Security
G8 Final Delivery
```

---

# 48. GATE MATRIX

| Gate | Required Evidence |
|---|---|
| G0 | Repository audit, owner decisions, assumptions, threat model |
| G1 | Auth, authorization, foundational tests |
| G2 | Catalog schema, price/availability integrity tests |
| G3 | Order state machine, concurrency, idempotency evidence |
| G4 | Preparation/pickup workflow evidence |
| G5 | Offline recovery and WhatsApp integration evidence |
| G6 | Security, privacy, accessibility, performance, migration evidence |
| G7 | Build, release, compatibility and security evidence |
| G8 | Final artifact, hashes, manifest, acceptance evidence |

A failed P0 requirement blocks progression.

---

# 49. SELF-AUDIT AFTER EVERY SENSITIVE PHASE

Before advancing, inspect:

```text
requirements
architecture
authorization
tenant isolation
data ownership
state machine
pricing correctness
availability correctness
duplicate behavior
replay behavior
offline behavior
migration impact
rollback/recovery
security
privacy
observability
cost
accessibility
localization
integration integrity
auditability
documentation
```

Any unresolved P0 issue blocks progression.

---

# 50. EXECUTION REPORT AFTER EVERY MATERIAL CHANGE

Record:

```text
What changed
Why
Requirement IDs satisfied
Files changed
API changes
Schema changes
Security impact
Privacy impact
Migration impact
Offline impact
Integration impact
Tests actually executed
Build actually executed
Actual outputs/evidence
Known limitations
Open questions
Owner decisions encountered
Rollback/recovery notes
PROJECT_STATE update
Next safe action
```

Do not write:

```text
everything is complete
fully tested
production ready
```

without evidence.

---

# 51. FIRST-ACTION PROTOCOL

## New Repository

The implementation agent MUST:

```text
1. Read this specification in full.
2. Inspect the repository.
3. Detect existing implementation.
4. Read PROJECT_STATE.md.
5. Read OPEN_QUESTIONS.md.
6. Read docs/DECISIONS.md.
7. Inventory toolchain/environment.
8. Establish G0.
9. Update project-control files.
10. Begin the smallest dependency-correct implementation slice.
```

## Existing Repository

Compare:

```text
specification
vs
repository
vs
runtime
vs
tests
```

Classify findings:

```text
compliant
partially compliant
contradictory
unsafe
obsolete
unknown
```

Do not overwrite working implementation blindly.

---

# 52. CHANGE CONTROL

Any change touching:

```text
catalog schema
price representation
availability rules
order state machine
authorization
authentication
local storage
sync protocol
API contract
WhatsApp integration
privacy
security
business policy
```

MUST explicitly answer:

```text
Does this affect existing data?
Does it affect old clients?
Does it require migration?
Is it backward-compatible?
What happens if interrupted?
What happens if the device loses network?
What happens if the process is killed?
What happens if an old client remains installed?
Can it be rolled back?
```

No silent breaking changes.

---

# 53. POLICY SNAPSHOTTING

Where historical order behavior depends on changing business policy, the relevant policy values MUST be snapshotted into the affected record.

Examples:

```text
price
currency
order acceptance rule
cancellation policy
availability interpretation
```

Historical orders MUST NOT be silently recalculated using today's policy.

---

# 54. SUPPORTING DATA CONTRACTS

Every major persistence entity MUST document:

```text
identity
ownership/store context
business fields
state
timestamps
version
audit linkage
privacy classification
retention
indexes
immutability rules
migration behavior
```

Derived values MUST NOT be mistaken for canonical truth.

---

# 55. FUTURE EVOLUTION

The architecture SHOULD permit future additions such as:

```text
online payment
pickup time slots
customer accounts
order substitution
promotions
loyalty
push notifications
official WhatsApp automation
POS/ERP synchronization
multi-branch management
advanced analytics
```

These are future capabilities, not V1 commitments.

Any future expansion SHOULD prefer additive and backward-compatible evolution.

---

# 56. EXPLICIT NON-OVERENGINEERING RULE

Jahhezly MUST NOT become an enterprise architecture exercise.

The implementation agent MUST resist:

```text
premature microservices
event-driven complexity without a need
distributed caches without measurement
multiple databases without evidence
complex search infrastructure
unnecessary orchestration
unnecessary realtime systems
```

The default principle is:

```text
simple architecture
+
strong invariants
+
good boundaries
+
measured evolution
```

---

# 57. FINAL ACCEPTANCE GATE

## Product

- Customer can browse the catalog.
- Cached catalog works under offline conditions where data exists.
- Prices are visible with freshness information.
- Customer can prepare a cart offline.
- Customer cannot mistake a local draft for a confirmed order.
- Orders reach the merchant workflow reliably.
- Merchant can prepare the order.
- Merchant can mark the order ready.
- Authorized merchant staff can complete pickup.
- Invalid state transitions are rejected.

## Data

- Prices are snapshot-safe.
- Order history preserves historical facts.
- Availability is authoritative.
- Local migrations preserve durable data.
- Backend migrations are controlled and recoverable.

## Security

- Merchant authorization is server-enforced.
- Tenant/store isolation is verified.
- IDOR-style access fails.
- Secrets are absent from client artifacts.
- Rate and abuse controls exist for public operations where required.
- Security-sensitive actions are auditable.

## Offline

- Catalog caching works.
- Cart persistence survives restart.
- Offline submission behavior is explicit.
- Synchronization is retry-safe.
- Duplicate order creation is prevented.

## WhatsApp

- Communication behavior is clearly defined.
- The app does not claim message delivery without evidence.
- WhatsApp failure does not corrupt order state.
- Provider-dependent functionality is disabled or verified honestly.

## UX

- Loading states exist.
- Empty states exist.
- Error states exist.
- Offline state exists.
- Stale data is visible.
- Accessibility requirements are tested.
- Localization behavior is tested.

## Operations

- Structured logs exist.
- Critical metrics exist.
- Sensitive information is redacted.
- Backup/restore strategy exists where backend data requires it.
- Cost-sensitive infrastructure is bounded.

## Release

- Real build artifact exists.
- Correct version/build identity exists.
- Artifact hash exists.
- Tests actually ran.
- Release manifest exists.
- Migration version exists.
- Known limitations are recorded.
- No private production secrets are included.

---

# 58. ARTIFACT TRUTH POLICY

Every artifact MUST be classified as:

```text
SOURCE
BUILD ARTIFACT
RELEASE ARTIFACT
TEST ARTIFACT
DOCUMENTATION ARTIFACT
```

An artifact may be called:

```text
built
exported
verified
released
```

only when it actually exists and evidence supports the claim.

Never fabricate:

```text
file paths
hashes
build results
test results
deployment results
provider delivery results
migration results
```

---

# 59. DELIVERY PACKAGE

The final project package SHOULD use:

```text
JAHHEZLY_<VERSION>_FINAL/
```

with a corresponding archive:

```text
JAHHEZLY_<VERSION>_FINAL.zip
```

Include:

```text
source
backend
configuration templates
tests
migration scripts
documentation
project-control files
localization resources
build configuration
release configuration templates
```

Never include:

```text
private signing keys
signing passwords
production secrets
service account private keys
personal credentials
machine-local disposable data
```

---

# 60. DELIVERY MANIFEST

`DELIVERY_MANIFEST.md` MUST record:

```text
Project name
Version
Build/version code
Git commit
Build timestamp
Toolchain versions
Platform target
API version
Schema version
Migration version
Build command
Artifact names
Artifact hashes
Tests executed
Security tests executed
Migration tests executed
Concurrency tests executed
Offline tests executed
Integration tests executed
Device/platform tests executed
Known limitations
Open questions
Excluded secrets
Rollback notes
Owner approvals
```

---

# 61. CHANGELOG DISCIPLINE

Every release MUST document:

```text
What changed
Why
Requirements affected
API changes
Schema changes
Migration changes
Security changes
Privacy changes
Offline behavior changes
Integration changes
Compatibility changes
Release changes
Known limitations
Rollback behavior
Owner approvals
```

Breaking changes MUST NOT be hidden inside a minor refactor.

---

# 62. VERSION-TO-VERSION RELEASE CONTRACT

Every significant release SHOULD follow:

```text
Old release
↓
Compatibility assessment
↓
Migration plan
↓
Backend compatibility changes
↓
New client/backend artifacts
↓
Migration verification
↓
Release
↓
Adoption observation
↓
Compatibility-window assessment
↓
Legacy behavior retirement only after explicit policy
```

Do not strand supported clients without a documented compatibility strategy.

---

# 63. GOLDEN RULES

The following are non-negotiable:

```text
1. Never guess sensitive owner decisions.
2. Never trust client authorization claims.
3. Never use cache as authoritative business truth.
4. Never accept a stale price as final without the applicable business confirmation.
5. Never silently accept unavailable products.
6. Never bypass the order state machine.
7. Never create duplicate orders because a response was lost.
8. Never treat WhatsApp opening as proof of delivery.
9. Never let WhatsApp failure corrupt authoritative order state.
10. Never rewrite finalized historical order facts.
11. Never use destructive reset as a normal update strategy.
12. Never ship real secrets inside the client.
13. Never expose tenant/store data across authorization boundaries.
14. Never claim a build/test/migration/integration succeeded without evidence.
15. Never weaken P0 controls because Jahhezly is an MVP.
16. Never introduce major infrastructure without demonstrated need.
17. Never silently change pricing policy semantics.
18. Never silently break supported clients.
19. Never store sensitive personal data merely because storage is available.
20. Never make offline UI appear more authoritative than it actually is.
21. Never use customer-entered identifiers as sole authorization proof.
22. Never assume a provider completed an action without provider evidence.
23. Never delete historical business facts to simplify implementation.
24. Never make the entire product dependent on continuous connectivity when the product requirement explicitly prioritizes offline resilience.
```

---

# 64. JAHHEZLY-SPECIFIC GOLDEN INVARIANTS

```text
JH-INVARIANT-01
The cached catalog is a convenience layer, not commercial truth.

JH-INVARIANT-02
Final order prices originate from authoritative backend validation.

JH-INVARIANT-03
Every accepted order item retains its accepted price snapshot.

JH-INVARIANT-04
Offline cart construction is always allowed to remain local.

JH-INVARIANT-05
Offline drafts are never presented as confirmed orders.

JH-INVARIANT-06
Order submission is idempotent.

JH-INVARIANT-07
Merchant operations are store/tenant authorized.

JH-INVARIANT-08
An order can only reach READY_FOR_PICKUP through an authorized merchant workflow.

JH-INVARIANT-09
An order can only reach COLLECTED through an authorized pickup-completion action.

JH-INVARIANT-10
WhatsApp is a communication channel, not a transactional source of truth.

JH-INVARIANT-11
The product remains operationally useful when network connectivity is unavailable.

JH-INVARIANT-12
A new release preserves durable user/local state unless an explicitly approved migration says otherwise.

JH-INVARIANT-13
Historical order facts are immutable or corrected through an auditable compensating mechanism.

JH-INVARIANT-14
Merchant price changes are auditable.

JH-INVARIANT-15
No customer-facing screen can claim freshness that the underlying data does not support.
```

---

# 65. REQUIREMENT TRACEABILITY

Every material requirement MUST receive a stable identifier.

Recommended prefixes:

```text
PROD-
CAT-
ORD-
OFF-
WAP-
MER-
AUTH-
SEC-
PRIV-
DATA-
API-
UX-
A11Y-
I18N-
PERF-
OPS-
TEST-
MIG-
REL-
COST-
AUD-
```

Every requirement MUST track:

```text
ID
Priority
Requirement
Source
Rationale
Dependencies
Architecture impact
Data impact
Authorization
Privacy impact
Migration impact
Implementation
Tests
Evidence
Status
Owner Decision
Release
```

Lifecycle:

```text
DISCOVERED
→ SPECIFIED
→ DESIGNED
→ IMPLEMENTED
→ TESTED
→ VERIFIED
→ RELEASED
→ MONITORED
```

---

# 66. INITIAL REQUIREMENTS BASELINE

| ID | Priority | Requirement |
|---|---|---|
| PROD-001 | P1 | Customer can browse a selected store catalog |
| PROD-002 | P1 | Customer can build a cart/list |
| CAT-001 | P0 | Authoritative current price exists server-side |
| CAT-002 | P0 | Historical accepted price is preserved |
| CAT-003 | P1 | Product availability is represented explicitly |
| OFF-001 | P1 | Cached catalog is usable offline |
| OFF-002 | P1 | Cart/draft survives temporary offline periods |
| OFF-003 | P0 | Offline drafts are never represented as confirmed orders |
| ORD-001 | P1 | Customer can submit an order |
| ORD-002 | P0 | Order submission is idempotent |
| ORD-003 | P0 | Server validates price and availability |
| ORD-004 | P1 | Merchant can accept/reject an order |
| ORD-005 | P1 | Merchant can prepare an order |
| ORD-006 | P1 | Merchant can mark order ready |
| ORD-007 | P1 | Merchant can mark order collected |
| WAP-001 | P1 | WhatsApp-assisted communication can be initiated |
| WAP-002 | P0 | WhatsApp initiation is not treated as delivery evidence |
| AUTH-001 | P0 | Merchant access is server-authorized |
| AUTH-002 | P0 | Tenant/store isolation is enforced |
| SEC-001 | P0 | No production secret is embedded in client |
| PRIV-001 | P1 | Personal data is minimized |
| DATA-001 | P0 | Historical order facts remain reconstructable |
| MIG-001 | P0 | Local schema changes are versioned and recoverable |
| REL-001 | P0 | Updates do not intentionally erase durable local state |
| TEST-001 | P0 | Critical workflows have automated tests |
| TEST-002 | P0 | Duplicate-order concurrency is tested |
| UX-001 | P1 | Offline/stale states are visible to the customer |
| UX-002 | P1 | Core workflows define loading/empty/error/success states |
| PERF-001 | P2 | Cached catalog interactions meet measured responsiveness targets |
| OPS-001 | P2 | Critical operations are observable |
| AUD-001 | P1 | Sensitive merchant/order transitions are auditable |

---

# 67. COMPLETION STANDARD

Jahhezly MUST NOT be considered complete merely because:

```text
screens exist
API exists
database exists
login works
```

It is complete only when the applicable contract is evidenced across:

```text
product
architecture
domain
security
privacy
data integrity
offline operation
WhatsApp boundary
testing
migration
updates
observability
release
acceptance
delivery
```

The implementation agent MUST prioritize:

```text
correctness
+
simplicity
+
security
+
data integrity
+
offline resilience
+
traceability
+
measurable evidence
+
truthful release status
```

over visual complexity or speculative architecture.

---

# 68. FINAL EXECUTION STANDARD

The final implementation should be able to survive:

```text
development
+
multiple implementation agents
+
daily catalog changes
+
price changes
+
weak network conditions
+
duplicate requests
+
concurrent merchant operations
+
application updates
+
schema evolution
+
provider changes
+
security review
+
testing
+
production incidents
```

without requiring the team to reconstruct missing requirements manually.

The system SHOULD remain small enough to understand while being disciplined enough to evolve.

---

# 69. END CONDITION

The Master Project Specification is considered structurally complete only when it provides:

```text
clear product identity
+
mission
+
scope
+
non-scope
+
authority
+
requirements
+
roles
+
tenant model
+
domain model
+
state machines
+
source-of-truth rules
+
offline architecture
+
data model
+
price/availability integrity
+
order integrity
+
authorization model
+
security model
+
privacy model
+
WhatsApp integration boundary
+
API contract
+
idempotency
+
concurrency controls
+
migration strategy
+
update strategy
+
testing strategy
+
observability
+
cost governance
+
release strategy
+
release gates
+
acceptance criteria
+
artifact truth
+
delivery contract
+
golden rules
```

No section may exist as filler.

The content under each section MUST be meaningful specifically for Jahhezly.

---

# 70. FINAL INSTRUCTION TO THE IMPLEMENTATION AGENT

Treat this document as the canonical implementation contract.

Do not replace product correctness with visual polish.

Do not replace authoritative data with cached state.

Do not replace explicit business decisions with guesses.

Do not replace evidence with plausible language.

Do not replace WhatsApp communication with a false transactional guarantee.

Do not replace offline resilience with a permanently connected assumption.

Do not replace a simple architecture with speculative enterprise infrastructure.

Build the smallest system that fully satisfies this contract.

When the repository, runtime, or external provider contradicts this specification:

```text
identify the contradiction
→ classify its severity
→ record the evidence
→ preserve P0 safety/integrity
→ update the appropriate control file
→ request owner decision when the conflict is business-sensitive
→ implement the smallest safe path
```

The goal is not merely to produce a functioning application.

The goal is to produce a **real, maintainable, auditable, update-safe, offline-resilient Click & Collect product whose implementation status can be proven from evidence**.

# END OF JAHHEZLY MASTER EXECUTION PROMPT
