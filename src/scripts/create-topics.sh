#!/bin/bash

set -e

KAFKA_BROKER=${KAFKA_BROKER:-localhost:9092}

echo "🔄 Aguardando Kafka em $KAFKA_BROKER..."

# Aguarda Kafka responder
while ! kafka-topics --bootstrap-server $KAFKA_BROKER --list >/dev/null 2>&1; do
  echo "⏳ Kafka não está pronto..."
  sleep 2
done

echo "✅ Kafka disponível!"

# Lista de tópicos
topics=(
  "pedidos"
  "pagamentos"
  "envios"
)

echo "📦 Criando tópicos..."

for topic in "${topics[@]}"; do
  echo "➡️  Verificando tópico: $topic"

  kafka-topics \
    --bootstrap-server $KAFKA_BROKER \
    --create \
    --if-not-exists \
    --topic $topic \
    --partitions 1 \
    --replication-factor 1

done

echo "🎉 Todos os tópicos estão prontos!"