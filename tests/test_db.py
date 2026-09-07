import asyncio

from src.core import db


def test_ping_e_init_models():
    asyncio.run(db.init_models())
    assert asyncio.run(db.ping()) is True
