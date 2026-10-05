# Jahhezly API

FastAPI modular-monolith backend.

```bash
pip install -e ".[dev]"
pytest -q
uvicorn app.main:app --reload
```

`JAHHEZLY_DB_URL` can point to PostgreSQL for a real server-backed run. Automated tests use SQLite.


## Demo scenario

The root `data/demo/` directory contains SYP-denominated, illustrative catalog and merchant records for the owner-authorized Paris Market and cham-center portfolio scenarios. Do not treat seeded prices as live retail data.


## Verification helpers

From `backend/`, the repository's end-to-end smoke scenario can be executed with:

```bash
python ../scripts/run_backend_smoke.py
```

It creates an isolated temporary SQLite database and exercises catalog read, guest order creation, idempotent replay, merchant login, all order transitions, and final collection.
