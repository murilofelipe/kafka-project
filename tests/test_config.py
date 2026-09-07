from src.core.config import Settings


def test_defaults():
    s = Settings(_env_file=None)
    assert s.kafka_broker == "localhost:9092"
    assert s.topic_pedidos == "pedidos"
    assert s.topic_dlq == "pedidos-dlq"
    assert s.retry_max == 3


def test_env_override(monkeypatch):
    monkeypatch.setenv("KAFKA_BROKER", "kafka:9092")
    monkeypatch.setenv("RETRY_MAX", "7")
    s = Settings(_env_file=None)
    assert s.kafka_broker == "kafka:9092"
    assert s.retry_max == 7
