import asyncio

from aiokafka import AIOKafkaProducer

from src.core.config import settings
from src.core.kafka_config import create_consumer, create_producer

STATUS_VALIDOS = {"CRIADO"}


async def processar_evento(evento: dict) -> None:
    """Processa um pedido. Levanta exceção em evento inválido (vai para retry/DLQ)."""
    pedido_id = evento.get("pedido_id")
    status = evento.get("status")
    if not pedido_id or status not in STATUS_VALIDOS:
        raise ValueError(f"Evento inválido: {evento}")
    print(f"💳 Processando pagamento do pedido {pedido_id}")


async def processar_com_retry(evento: dict, dlq: AIOKafkaProducer) -> None:
    """Tenta processar com backoff exponencial; após retry_max falhas, manda para a DLQ."""
    for tentativa in range(1, settings.retry_max + 1):
        try:
            await processar_evento(evento)
            return
        except Exception as exc:  # noqa: BLE001 - qualquer falha de processamento vira retry
            if tentativa == settings.retry_max:
                print(f"❌ Falhou após {tentativa} tentativas, enviando para DLQ: {exc}")
                await dlq.send_and_wait(settings.topic_dlq, evento)
                return
            espera = settings.retry_backoff_base_seconds * 2 ** (tentativa - 1)
            print(f"⚠️  Tentativa {tentativa} falhou ({exc}); retry em {espera}s")
            await asyncio.sleep(espera)


async def main() -> None:
    consumer = await create_consumer(settings.topic_pedidos, settings.consumer_group)
    dlq = await create_producer()
    print("🟢 Consumer iniciado... 👀 Aguardando mensagens...")
    try:
        async for msg in consumer:
            await processar_com_retry(msg.value, dlq)
    finally:
        await consumer.stop()
        await dlq.stop()


if __name__ == "__main__":
    asyncio.run(main())
