# ===============================
# 🐳 Docker Commands
# ===============================

up:
	@echo "🚀 Subindo containers..."
	docker compose up --build

up-d:
	@echo "🚀 Subindo containers em background..."
	docker compose up --build -d

down:
	@echo "🛑 Parando containers..."
	docker compose down

clean:
	@echo "🧹 Limpando tudo (containers + volumes)..."
	docker compose down -v

logs:
	@echo "📜 Logs gerais..."
	docker compose logs -f

logs-api:
	@echo "📜 Logs da API..."
	docker compose logs -f api

logs-consumer:
	@echo "📜 Logs do consumer..."
	docker compose logs -f consumer


# ===============================
# 🔁 Testes rápidos
# ===============================

send:
	@echo "📤 Enviando evento de teste..."
	curl -X POST http://localhost:8000/pedido


# ===============================
# 🧠 Kafka Debug
# ===============================

kafka-shell:
	@echo "🔧 Acessando container Kafka..."
	docker exec -it kafka bash

consumer-groups:
	@echo "📊 Listando consumer groups..."
	docker exec -it kafka kafka-consumer-groups --bootstrap-server localhost:9092 --list

describe-group:
	@echo "📊 Detalhando grupo pagamento-service..."
	docker exec -it kafka kafka-consumer-groups \
	--bootstrap-server localhost:9092 \
	--describe \
	--group pagamento-service


# ===============================
# 🧩 Ajuda
# ===============================

help:
	@echo ""
	@echo "📦 Comandos disponíveis:"
	@echo " make up             - sobe containers"
	@echo " make up-d           - sobe em background"
	@echo " make down           - para containers"
	@echo " make clean          - remove tudo (inclui volumes)"
	@echo " make logs           - logs gerais"
	@echo " make logs-api       - logs da API"
	@echo " make logs-consumer  - logs do consumer"
	@echo " make send           - envia evento de teste"
	@echo " make kafka-shell    - acessa Kafka"
	@echo " make consumer-groups- lista grupos"
	@echo " make describe-group - detalhes do group"
	@echo ""