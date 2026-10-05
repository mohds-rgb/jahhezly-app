# Security Design

Threats prioritized:

- broken access control
- tenant breakout / IDOR
- privilege escalation
- price tampering
- availability manipulation
- order state tampering
- replay/duplicate submissions
- secret leakage
- data exposure
- unsafe WhatsApp hand-off

Controls:

- JWT bearer authentication with expiry
- server-side membership lookup
- role capability mapping
- scrypt password hashing
- Pydantic request validation
- idempotency persistence
- conditional versioned updates
- audit events
- environment-only secrets
