import asyncio

from src.consumer import worker


def test_processar_evento_criado(capsys):
    asyncio.run(worker.processar_evento({"pedido_id": "p1", "status": "CRIADO"}))
    out = capsys.readouterr().out
    assert "Processando pagamento do pedido p1" in out


def test_processar_evento_outro_status(capsys):
    asyncio.run(worker.processar_evento({"pedido_id": "p2", "status": "OUTRO"}))
    out = capsys.readouterr().out
    assert "Processando pagamento" not in out
