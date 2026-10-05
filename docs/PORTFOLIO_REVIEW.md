# Portfolio Review Notes

## What a reviewer should notice

1. The project has explicit ownership and a proprietary license.
2. The two named merchants are owner-authorized scenario data, not fabricated customer claims.
3. The code focuses on the difficult parts of the workflow: price integrity, availability, idempotency, concurrency, tenant isolation, offline state, and auditability.
4. Owner-reported historical numbers are isolated from engineering verification evidence.
5. Production claims are deliberately absent where runtime proof is unavailable.

## Suggested interview walkthrough

Start with the order submission path, then explain why the cached price cannot be trusted, how idempotency prevents duplicate orders, how merchant branch membership is authorized server-side, and how an offline draft differs from a confirmed backend order.
