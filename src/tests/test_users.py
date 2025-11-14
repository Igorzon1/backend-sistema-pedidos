# tests/test_users.py
import pytest

@pytest.mark.asyncio
async def test_create_user(async_client, fake_db):
    payload = {"name": "Igorzon", "email": "igor@example.com"}
    resp = await async_client.post("/users/", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert "user" in data
    assert data["user"]["email"] == payload["email"]
    assert data["user"]["name"] == payload["name"]

@pytest.mark.asyncio
async def test_create_user_conflict(async_client, fake_db):
    payload = {"name": "Igorzon", "email": "igor@example.com"}
    r1 = await async_client.post("/users/", json=payload)
    assert r1.status_code == 201
    r2 = await async_client.post("/users/", json=payload)
    assert r2.status_code == 409

@pytest.mark.asyncio
async def test_list_users(async_client, fake_db):
    # cria dois usuários via endpoint
    await async_client.post("/users/", json={"name": "A", "email": "a@example.com"})
    await async_client.post("/users/", json={"name": "B", "email": "b@example.com"})
    r = await async_client.get("/users/")
    assert r.status_code == 200
    data = r.json()
    assert data["count"] == 2
    emails = {u["email"] for u in data["users"]}
    assert {"a@example.com", "b@example.com"}.issubset(emails)
