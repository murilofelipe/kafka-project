"""Fábricas de Producer/Consumer Kafka assíncronos (aiokafka)."""

import asyncio
import json

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer

from src.core.config import settings


def _serialize(value: dict) -> bytes:
    return json.dumps(value).encode("utf-8")


def _deserialize(raw: bytes) -> dict:
    return json.loads(raw.decode("utf-8"))


async def create_producer(retries: int = 10) -> AIOKafkaProducer:
    """Cria e inicia um producer, tentando reconectar enquanto o broker sobe."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        producer = AIOKafkaProducer(
            bootstrap_servers=settings.kafka_broker,
            value_serializer=_serialize,
        )
        try:
            await producer.start()
            print("✅ Producer conectado ao Kafka!")
            return producer
        except Exception as exc:  # noqa: BLE001 - broker ainda subindo
            last_error = exc
            print(f"Kafka indisponível ({attempt}/{retries}), retry em 2s... ({exc})")
            await producer.stop()
            await asyncio.sleep(2)
    raise RuntimeError(f"Não conseguiu conectar o producer ao Kafka: {last_error}")


async def create_consumer(topic: str, group_id: str, retries: int = 10) -> AIOKafkaConsumer:
    """Cria e inicia um consumer inscrito em ``topic``."""
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=settings.kafka_broker,
            group_id=group_id,
            value_deserializer=_deserialize,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )
        try:
            await consumer.start()
            print("✅ Consumer conectado ao Kafka!")
            return consumer
        except Exception as exc:  # noqa: BLE001 - broker ainda subindo
            last_error = exc
            print(f"Kafka indisponível ({attempt}/{retries}), retry em 2s... ({exc})")
            await consumer.stop()
            await asyncio.sleep(2)
    raise RuntimeError(f"Não conseguiu conectar o consumer ao Kafka: {last_error}")
