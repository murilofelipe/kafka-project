import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.core.config import settings
from src.core.db import init_models
from src.core.kafka_config import create_producer
from src.core.pedidos import criar_pedido as persistir_pedido


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_models()
    app.state.producer = await create_producer()
    try:
        yield
    finally:
        await app.state.producer.stop()


app = FastAPI(lifespan=lifespan)


@app.post("/pedido")
async def criar_pedido():
    pedido = {"pedido_id": str(uuid.uuid4()), "status": "CRIADO"}

    await persistir_pedido(pedido["pedido_id"])
    print("📤 Enviando evento:", pedido)
    await app.state.producer.send_and_wait(settings.topic_pedidos, pedido)

    return {"message": "Pedido enviado para processamento", "pedido": pedido}
