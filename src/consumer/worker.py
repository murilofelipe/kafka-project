from src.core.kafka_config import get_consumer

consumer = get_consumer("pedidos", "pagamento-service")

print("🟢 Consumer iniciado...")
print("👀 Aguardando mensagens...")

while True:
    records = consumer.poll(timeout_ms=1000)

    if not records:
        print("⏳ Nenhuma mensagem...")
        continue

    for topic_partition, messages in records.items():
        for msg in messages:
            print("🔥 Mensagem crua:", msg)

            evento = msg.value

            print(f"📦 Evento recebido: {evento}")

            if evento.get("status") == "CRIADO":
                print(f"💳 Processando pagamento do pedido {evento['pedido_id']}")