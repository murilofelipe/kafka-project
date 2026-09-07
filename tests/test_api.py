from unittest.mock import AsyncMock

import pytest
from fastapi.testclient import TestClient

from src.api import main


@pytest.fixture
def client(monkeypatch):
    fake_producer = AsyncMock()
    monkeypatch.setattr(main, "create_producer", AsyncMock(return_value=fake_producer))
    with TestClient(main.app) as c:
        c.fake_producer = fake_producer
        yield c


def test_criar_pedido_publica_evento(client):
    resp = client.post("/pedido")
    assert resp.status_code == 200
    body = resp.json()
    assert body["pedido"]["status"] == "CRIADO"
    assert "pedido_id" in body["pedido"]

    client.fake_producer.send_and_wait.assert_awaited_once()
    topic, evento = client.fake_producer.send_and_wait.await_args.args
    assert topic == "pedidos"
    assert evento["pedido_id"] == body["pedido"]["pedido_id"]


def test_health_ok(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "checks": {"kafka": True, "database": True}}


def test_health_degraded_quando_kafka_cai(client):
    client.fake_producer.client.fetch_all_metadata.side_effect = OSError("down")
    resp = client.get("/health")
    assert resp.status_code == 503
    assert resp.json()["checks"]["kafka"] is False
