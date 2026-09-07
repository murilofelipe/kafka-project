import asyncio

from src.core.config import settings
from src.core.kafka_config import create_consumer


async def processar_evento(evento: dict) -> None:
    print(f"📦 Evento recebido: {evento}")
    if evento.get("status") == "CRIADO":
        print(f"💳 Processando pagamento do pedido {evento['pedido_id']}")


async def main() -> None:
    consumer = await create_consumer(settings.topic_pedidos, settings.consumer_group)
    print("🟢 Consumer iniciado... 👀 Aguardando mensagens...")
    try:
        async for msg in consumer:
            await processar_evento(msg.value)
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
