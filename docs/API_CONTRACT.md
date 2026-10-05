# API Contract

API version: `v1`

## Error model

```json
{
  "code": "PRICE_CHANGED",
  "message": "The product price changed.",
  "details": {}
}
```

Stable codes include:

```text
UNAUTHORIZED
FORBIDDEN
RESOURCE_NOT_FOUND
INVALID_REQUEST
CONFLICT
PRICE_CHANGED
PRODUCT_UNAVAILABLE
INVALID_STATE_TRANSITION
SERVICE_UNAVAILABLE
```

## Customer

```http
GET  /v1/stores
GET  /v1/stores/{store_id}/catalog
GET  /v1/stores/{store_id}/categories
POST /v1/orders
GET  /v1/orders/{order_id}
POST /v1/orders/{order_id}/cancel
```

Order creation requires:

```http
X-Idempotency-Key: <stable-request-key>
X-Guest-Session: <opaque-client-session>
```

The request may include `customerPhone`, which is normalized and stored only as an order contact field.

The server validates store ownership, product identity, availability, current price, and request shape before creating an order.

`GET /v1/orders/{order_id}` requires the same guest session used for anonymous creation.

`POST /v1/orders/{order_id}/cancel` uses optimistic concurrency through `If-Match: <order-version>` and is currently allowed only for cancellable states defined by the domain state machine.

## Merchant

All merchant routes require:

```http
Authorization: Bearer <JWT>
```

The JWT carries identity, not authoritative store role/capabilities. Server-side membership lookup determines access.

```http
GET  /v1/merchant/me
GET  /v1/merchant/orders?store_id=<id>
GET  /v1/merchant/orders/{id}
POST /v1/merchant/orders/{id}/accept
POST /v1/merchant/orders/{id}/reject
POST /v1/merchant/orders/{id}/start-preparing
POST /v1/merchant/orders/{id}/ready
POST /v1/merchant/orders/{id}/collect
POST /v1/merchant/catalog/products
PATCH /v1/merchant/catalog/products/{id}
POST /v1/merchant/catalog/products/{id}/price
POST /v1/merchant/catalog/products/{id}/availability
```

Order mutations require:

```http
If-Match: <order-version>
```

A stale version fails closed with `409 CONFLICT`.

## Store context

`GET /v1/stores` returns optional `city`, `district`, and `branchCode` fields. These fields are informational; merchant authorization still comes from authenticated server-side memberships.

## Localized catalog fields

Catalog responses expose optional `nameAr`, `descriptionAr`, and `categoryAr` alongside canonical English fields.
