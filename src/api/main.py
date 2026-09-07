import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from src.core.config import settings
from src.core.db import init_models
from src.core.db import ping as db_ping
from src.core.kafka_config import create_producer
from src.core.logging_config import get_logger, setup_logging
from src.core.pedidos import criar_pedido as persistir_pedido

setup_logging()
log = get_logger("api")


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
    log.info("evento publicado", extra={"pedido_id": pedido["pedido_id"]})
    await app.state.producer.send_and_wait(settings.topic_pedidos, pedido)

    return {"message": "Pedido enviado para processamento", "pedido": pedido}


@app.get("/health")
async def health(response: Response):
    checks = {"kafka": False, "database": False}
    try:
        await app.state.producer.client.fetch_all_metadata()
        checks["kafka"] = True
    except Exception:  # noqa: BLE001 - health check nunca levanta
        log.warning("health: kafka indisponível", exc_info=True)
    try:
        checks["database"] = await db_ping()
    except Exception:  # noqa: BLE001
        log.warning("health: banco indisponível", exc_info=True)

    status = "ok" if all(checks.values()) else "degraded"
    if status != "ok":
        response.status_code = 503
    return {"status": status, "checks": checks}
