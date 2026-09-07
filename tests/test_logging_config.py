import json
import logging

from src.core.logging_config import JsonFormatter


def test_json_formatter_inclui_extras():
    rec = logging.LogRecord("api", logging.INFO, __file__, 1, "oi", (), None)
    rec.pedido_id = "abc"
    out = json.loads(JsonFormatter().format(rec))
    assert out["msg"] == "oi"
    assert out["level"] == "INFO"
    assert out["pedido_id"] == "abc"
