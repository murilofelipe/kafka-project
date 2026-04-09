from kafka import KafkaProducer, KafkaConsumer
import json
import os
import time

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "localhost:9092")


def get_producer():
    for i in range(10):
        try:
            print(f"Tentando conectar ao Kafka ({i+1}/10)...")
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode("utf-8")
            )
            print("✅ Conectado ao Kafka!")
            return producer
        except Exception as e:
            print(f"Kafka indisponível, retry em 2s... ({e})")
            time.sleep(2)

    raise Exception("❌ Não conseguiu conectar ao Kafka")

def get_consumer(topic, group_id):
    for i in range(10):
        try:
            print(f"Tentando conectar consumer ({i+1}/10)...")
            consumer = KafkaConsumer(
                bootstrap_servers=KAFKA_BROKER,
                group_id=group_id,
                value_deserializer=lambda x: json.loads(x.decode("utf-8")),
                auto_offset_reset="earliest",
                enable_auto_commit=True,
            )

            consumer.subscribe([topic])
            print("✅ Consumer conectado!")
            return consumer
        except Exception as e:
            print(f"Kafka indisponível, retry em 2s... ({e})")
            time.sleep(2)

    raise Exception("❌ Consumer não conseguiu conectar ao Kafka")