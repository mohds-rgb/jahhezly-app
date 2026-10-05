# Product Surface Inventory

| Surface | Actor | Source | Offline |
|---|---|---|---|
| Store Selection | Customer | API/local | Read cache |
| Catalog | Customer | Local/backend | Yes |
| Product Detail | Customer | Local/backend | Yes |
| Cart | Customer | SQLite | Yes |
| Order Review | Customer | Local + backend validation | Partial |
| Order Status | Customer | Backend/local | Cached read |
| Merchant Login | Merchant | Backend | No |
| Incoming Orders | Merchant | Backend | No |
| Preparation | Merchant | Backend | No |
| Catalog Management | Manager | Backend | No |
| Price Management | Manager | Backend | No |
| Availability | Manager | Backend | No |
