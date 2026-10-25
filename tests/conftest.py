
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import get_settings
from app.db.session import get_db
from app.main import app


@pytest.fixture
def test_client():
    test_engine = create_engine(
        get_settings().test_database_url,
        pool_pre_ping=True,
    )

    connection = test_engine.connect()
    transaction = connection.begin()

    TestingSessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
        join_transaction_mode="create_savepoint",
    )

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as client:
            yield client
    finally:
        app.dependency_overrides.clear()
        transaction.rollback()
        connection.close()
        test_engine.dispose()


@pytest.fixture
def authenticated_client(test_client):
    email = "customer-test@example.com"
    password = "TestPassword123!"

    registration = test_client.post(
        "/api/v1/auth/register",
        json={
            "name": "Customer Test User",
            "email": email,
            "password": password,
        },
    )
    assert registration.status_code == 201

    login = test_client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert login.status_code == 200

    token = login.json()["access_token"]
    test_client.headers.update(
        {"Authorization": f"Bearer {token}"}
    )

    return test_client
