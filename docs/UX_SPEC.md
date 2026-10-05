# UX Specification

Jahhezly should feel fast, simple, predictable, quiet, lightweight and obvious.

Critical customer flows define:

```text
loading
empty
success
failure
retry
offline
timeout
stale
conflict
duplicate action
```

A stale catalog price is visibly marked as cached/stale.

Offline order submission is represented as:

```text
Saved locally → Queued → Waiting for connection
```

Only backend acknowledgement changes the order to `SUBMITTED`.

Merchant surfaces prioritize operational scanning: state, age, item count, store and next action.
