"""Operações de persistência do estado do pedido."""

from src.core.db import SessionLocal
from src.core.models import Pedido


async def criar_pedido(pedido_id: str, status: str = "PENDENTE") -> None:
    async with SessionLocal() as session:
        session.add(Pedido(id=pedido_id, status=status))
        await session.commit()


async def atualizar_status(pedido_id: str, status: str) -> None:
    async with SessionLocal() as session:
        pedido = await session.get(Pedido, pedido_id)
        if pedido is None:
            return
        pedido.status = status
        await session.commit()
