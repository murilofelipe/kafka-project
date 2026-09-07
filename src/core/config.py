"""Configuração central da aplicação via variáveis de ambiente (Pydantic Settings)."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Kafka
    kafka_broker: str = "localhost:9092"
    topic_pedidos: str = "pedidos"
    topic_dlq: str = "pedidos-dlq"
    consumer_group: str = "pagamento-service"

    # Retry / DLQ (Story 2.2)
    retry_max: int = 3
    retry_backoff_base_seconds: float = 1.0

    # Banco de dados (Story 3.x)
    database_url: str = "sqlite+aiosqlite:///./kafka_project.db"


settings = Settings()
