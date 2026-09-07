import asyncio

from src.core import db, pedidos
from src.core.models import Pedido


def test_criar_e_atualizar_status():
    async def cenario():
        await db.init_models()
        await pedidos.criar_pedido("t-123")
        async with db.SessionLocal() as s:
            assert (await s.get(Pedido, "t-123")).status == "PENDENTE"
        await pedidos.atualizar_status("t-123", "PAGO")
        async with db.SessionLocal() as s:
            assert (await s.get(Pedido, "t-123")).status == "PAGO"

    asyncio.run(cenario())
