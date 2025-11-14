# tests/test_orders.py
import pytest

@pytest.mark.asyncio
async def test_create_order_success(async_client, fake_db, monkeypatch):
    # mock do charge_card para sucesso
    import app.services.payment_client as pc

    async def fake_charge(user_id: str, amount: float):
        return {"success": True, "ref": "PAY-FAKE-123"}

    monkeypatch.setattr("app.api.orders.charge_card", fake_charge)

    # cria user primeiro (para user_id válido)
    u = await async_client.post("/users/", json={"name": "Igor", "email": "igororder@example.com"})
    assert u.status_code == 201
    user_id = u.json()["user"]["id"]

    payload = {"user_id": user_id, "amount": 12.34}
    r = await async_client.post("/orders/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert data["status"] == "created"
    assert "order_id" in data

@pytest.mark.asyncio
async def test_create_order_payment_failed(async_client, fake_db, monkeypatch):
    # mock do charge_card para falha
    import app.services.payment_client as pc

    async def fake_charge_fail(user_id: str, amount: float):
        return {"success": False, "error": "simulated failure"}

    monkeypatch.setattr("app.api.orders.charge_card", fake_charge_fail)

    # cria user
    u = await async_client.post("/users/", json={"name": "X", "email": "x@example.com"})
    assert u.status_code == 201
    user_id = u.json()["user"]["id"]

    payload = {"user_id": user_id, "amount": 50.0}
    r = await async_client.post("/orders/", json=payload)
    assert r.status_code == 400
