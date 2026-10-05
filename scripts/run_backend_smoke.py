from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1] / "backend"
if str(BACKEND) not in sys.path:
    sys.path.insert(0, str(BACKEND))


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        db_path = Path(tmp) / "smoke.db"
        os.environ["JAHHEZLY_DB_URL"] = f"sqlite:///{db_path}"
        os.environ["JAHHEZLY_JWT_SECRET"] = "smoke-test-secret-with-more-than-32-bytes-2026"
        os.environ["JAHHEZLY_ALLOW_GUEST_ORDERS"] = "true"
        os.environ["JAHHEZLY_DEMO_STAFF_PASSWORD"] = "Smoke-Demo-Password-123!"

        from fastapi.testclient import TestClient
        from app.main import app
        from app.seed_demo import seed
        from app.db import SessionLocal
        from app.models import Order
        from sqlalchemy import select

        seed()

        with TestClient(app) as client:
            stores = client.get("/v1/stores")
            assert stores.status_code == 200 and len(stores.json()) == 5
            paris = next(store for store in stores.json() if store["name"] == "Paris Market — Basra")

            catalog = client.get(f"/v1/stores/{paris['id']}/catalog")
            assert catalog.status_code == 200 and catalog.json()
            item = next(entry for entry in catalog.json() if entry["availability"] == "AVAILABLE")

            headers = {
                "X-Idempotency-Key": "smoke-order-001",
                "X-Guest-Session": "smoke-guest-001",
            }
            order = client.post(
                "/v1/orders",
                json={
                    "storeId": paris["id"],
                    "customerPhone": "+963944000000",
                    "items": [
                        {
                            "productId": item["id"],
                            "quantity": 1,
                            "clientUnitPrice": str(item["price"]),
                        }
                    ],
                },
                headers=headers,
            )
            assert order.status_code == 201
            order_payload = order.json()
            assert order_payload["state"] == "SUBMITTED"
            assert order_payload["customerPhone"] == "+963944000000"

            replay = client.post(
                "/v1/orders",
                json={
                    "storeId": paris["id"],
                    "customerPhone": "+963944000000",
                    "items": [
                        {
                            "productId": item["id"],
                            "quantity": 1,
                            "clientUnitPrice": str(item["price"]),
                        }
                    ],
                },
                headers=headers,
            )
            assert replay.status_code == 201 and replay.json() == order_payload

            login = client.post(
                "/v1/auth/login",
                json={"email": "demo.manager@jahhezly.local", "password": os.environ["JAHHEZLY_DEMO_STAFF_PASSWORD"]},
            )
            assert login.status_code == 200
            auth = {"Authorization": f"Bearer {login.json()['accessToken']}"}

            current = order_payload
            for action in ("accept", "start-preparing", "ready", "collect"):
                response = client.post(
                    f"/v1/merchant/orders/{current['id']}/{action}",
                    headers={**auth, "If-Match": str(current["version"])},
                )
                assert response.status_code == 200, response.text
                current = response.json()

            assert current["state"] == "COLLECTED"

        with SessionLocal() as db:
            assert len(db.scalars(select(Order)).all()) == 1

        print("BACKEND_SMOKE_OK")


if __name__ == "__main__":
    main()
