import asyncio
import time

from aiokafka import AIOKafkaProducer

from src.core.config import settings
from src.core.db import init_models
from src.core.kafka_config import create_consumer, create_producer
from src.core.logging_config import get_logger, setup_logging
from src.core.pedidos import atualizar_status

setup_logging()
log = get_logger("consumer")

STATUS_VALIDOS = {"CRIADO"}


async def processar_evento(evento: dict) -> None:
    """Processa um pedido. Levanta exceção em evento inválido (vai para retry/DLQ)."""
    pedido_id = evento.get("pedido_id")
    status = evento.get("status")
    if not pedido_id or status not in STATUS_VALIDOS:
        raise ValueError(f"Evento inválido: {evento}")
    log.info("processando pagamento", extra={"pedido_id": pedido_id})


async def processar_com_retry(evento: dict, dlq: AIOKafkaProducer) -> None:
    """Tenta processar com backoff exponencial; após retry_max falhas, manda para a DLQ."""
    pedido_id = evento.get("pedido_id")
    inicio = time.monotonic()
    for tentativa in range(1, settings.retry_max + 1):
        try:
            await processar_evento(evento)
            await atualizar_status(evento["pedido_id"], "PAGO")
            log.info(
                "pedido pago",
                extra={
                    "pedido_id": pedido_id,
                    "duracao_ms": round((time.monotonic() - inicio) * 1000),
                },
            )
            return
        except Exception as exc:  # noqa: BLE001 - qualquer falha de processamento vira retry
            if tentativa == settings.retry_max:
                log.error(
                    "esgotou retries, enviando para DLQ",
                    extra={"pedido_id": pedido_id, "tentativas": tentativa, "erro": str(exc)},
                )
                if pedido_id:
                    await atualizar_status(pedido_id, "FALHADO")
                await dlq.send_and_wait(settings.topic_dlq, evento)
                return
            espera = settings.retry_backoff_base_seconds * 2 ** (tentativa - 1)
            log.warning(
                "tentativa falhou",
                extra={"pedido_id": pedido_id, "tentativa": tentativa, "retry_em_s": espera},
            )
            await asyncio.sleep(espera)


async def main() -> None:
    await init_models()
    consumer = await create_consumer(settings.topic_pedidos, settings.consumer_group)
    dlq = await create_producer()
    log.info("consumer iniciado, aguardando mensagens")
    try:
        async for msg in consumer:
            await processar_com_retry(msg.value, dlq)
    finally:
        await consumer.stop()
        await dlq.stop()


if __name__ == "__main__":
    asyncio.run(main())
