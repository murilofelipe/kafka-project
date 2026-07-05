#!/usr/bin/env python3
"""PreToolUse guard for the Kafka project repo.

Rules:
  1. Never edit `.env` files.
"""
import json
import os
import sys


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return 0

    file_path = data.get("tool_input", {}).get("file_path", "") or ""
    if not file_path:
        return 0

    base = os.path.basename(file_path)

    if base == ".env" or (base.endswith(".env") and not base.endswith(".example")):
        sys.stderr.write(
            "Bloqueado: arquivos .env contem segredos e nao devem ser editados "
            "pelo agente. Edite manualmente se realmente necessario.\n"
        )
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
