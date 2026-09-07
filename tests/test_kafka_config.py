import asyncio

import pytest

from src.core import kafka_config


def test_serialize_roundtrip():
    payload = {"pedido_id": "abc", "status": "CRIADO"}
    assert kafka_config._deserialize(kafka_config._serialize(payload)) == payload


def test_create_producer_desiste_apos_retries(monkeypatch):
    class FakeProducer:
        def __init__(self, *a, **kw): ...
        async def start(self):
            raise OSError("broker down")

        async def stop(self): ...

    monkeypatch.setattr(kafka_config, "AIOKafkaProducer", FakeProducer)
    monkeypatch.setattr(kafka_config.asyncio, "sleep", lambda *_: asyncio.sleep(0))

    with pytest.raises(RuntimeError):
        asyncio.run(kafka_config.create_producer(retries=2))
