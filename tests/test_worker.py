import asyncio
from unittest.mock import AsyncMock

import pytest

from src.consumer import worker


def test_processar_evento_criado(caplog):
    with caplog.at_level("INFO"):
        asyncio.run(worker.processar_evento({"pedido_id": "p1", "status": "CRIADO"}))
    assert any(r.pedido_id == "p1" for r in caplog.records)


def test_processar_evento_invalido_levanta():
    with pytest.raises(ValueError):
        asyncio.run(worker.processar_evento({"pedido_id": "p2", "status": "OUTRO"}))


def test_retry_sucesso_marca_pago(monkeypatch):
    monkeypatch.setattr(worker, "atualizar_status", AsyncMock())
    dlq = AsyncMock()
    asyncio.run(worker.processar_com_retry({"pedido_id": "p1", "status": "CRIADO"}, dlq))
    dlq.send_and_wait.assert_not_awaited()
    worker.atualizar_status.assert_awaited_once_with("p1", "PAGO")


def test_retry_esgota_marca_falhado_e_envia_para_dlq(monkeypatch):
    monkeypatch.setattr(worker.settings, "retry_max", 3)
    monkeypatch.setattr(worker.settings, "retry_backoff_base_seconds", 0)
    monkeypatch.setattr(worker, "atualizar_status", AsyncMock())
    dlq = AsyncMock()
    evento = {"pedido_id": "p9", "status": "INVALIDO"}
    asyncio.run(worker.processar_com_retry(evento, dlq))
    worker.atualizar_status.assert_awaited_once_with("p9", "FALHADO")
    dlq.send_and_wait.assert_awaited_once_with("pedidos-dlq", evento)
