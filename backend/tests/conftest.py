import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["JAHHEZLY_DB_URL"] = "sqlite://"
os.environ["JAHHEZLY_JWT_SECRET"] = "test-secret-only-32-bytes-minimum-value"
os.environ["JAHHEZLY_ALLOW_GUEST_ORDERS"] = "true"

from app.db import Base, get_db
from app.main import app

@pytest.fixture()
def db_engine():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    try:
        yield engine
    finally:
        Base.metadata.drop_all(bind=engine)
        engine.dispose()

@pytest.fixture()
def db(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture()
def client(db):
    def override():
        yield db
    app.dependency_overrides[get_db] = override
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture()
def seeded(db):
    from tests.factories import seed_graph
    result = seed_graph(db)
    result["db"] = db
    return result
