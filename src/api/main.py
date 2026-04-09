from fastapi import FastAPI
from src.core.kafka_config import get_producer
import uuid

app = FastAPI()

producer = None


@app.on_event("startup")
def startup_event():
    global producer
    producer = get_producer()


@app.post("/pedido")
def criar_pedido():
    pedido = {
        "pedido_id": str(uuid.uuid4()),
        "status": "CRIADO"
    }

    print("📤 Enviando evento:", pedido)

    producer.send("pedidos", pedido)
    producer.flush()

    return {
        "message": "Pedido enviado para processamento",
        "pedido": pedido
    }