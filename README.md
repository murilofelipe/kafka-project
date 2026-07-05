# 🚀 Kafka Event-Driven Project

Projeto simples para estudo de arquitetura orientada a eventos utilizando **Apache Kafka**, **Python (FastAPI)** e **Docker**.

---

## 🧠 Objetivo

Demonstrar um fluxo básico de mensageria desacoplada:

```text
API (Producer) → Kafka → Consumer
```

---

## 🧩 Arquitetura

- **API (FastAPI)** → produz eventos (`pedido`)
- **Kafka (KRaft mode)** → broker de eventos (sem Zookeeper)
- **Consumer (Worker)** → consome e processa eventos

---

## 📂 Estrutura do Projeto

```
src/
├── api/ # API (producer)
├── consumer/ # worker (consumer)
├── core/ # configuração Kafka
└── scripts/ # scripts auxiliares (ex: criação de tópicos)
```

---

## ⚙️ Requisitos

- Docker
- Docker Compose
- Make (opcional, mas recomendado)

---

## 🚀 Como rodar

### Subir o ambiente

```
make up
```

### Rodar em background

```
make up-d
```

### Parar containers

```
make down
```

### Limpar tudo (incluindo volumes)

```
make clean
```

---

## 📤 Enviar evento de teste

```
make send
```

ou manualmente:

```
curl -X POST http://localhost:8000/pedido
```

---

## 📜 Logs

### Consumer

```
make logs-consumer
```

### API

```
make logs-api
```

### Todos

```
make logs
```

---

## 📬 Exemplo de fluxo

1. Cliente faz requisição:

```
POST /pedido
```

2. API publica evento no Kafka:

```json
{
  "pedido_id": "uuid",
  "status": "CRIADO"
}
Consumer processa:
📦 Evento recebido: {...}
💳 Processando pagamento do pedido ...
```

## 🧠 Conceitos aplicados

- Event-Driven Architecture
- Producer / Consumer Pattern
- Kafka Topics
- Consumer Groups
- Offset Management
- Comunicação assíncrona
- Dockerização de serviços

---

## ⚠️ Observações importantes

- Uso de `PYTHONUNBUFFERED=1` para evitar buffering de logs no Docker
- Kafka rodando em modo **KRaft (sem Zookeeper)**
- Tópicos criados automaticamente via script de inicialização
- Consumer configurado com `auto_offset_reset=earliest`

---

## 🔧 Debug e inspeção

Listar consumer groups:

```
make consumer-groups
```

Detalhar grupo:

```
make describe-group
```

Acessar container Kafka:

```
make kafka-shell
```

---

## 📋 Backlog de Melhorias

Para guiar a evolução deste projeto de um protótipo de estudo para um serviço pronto para produção, criamos um planejamento detalhado de melhorias estruturado em formato de backlog. 

O planejamento completo está disponível no arquivo [BACKLOG.md](file:///home/work/Documentos/Github/kafka-project/BACKLOG.md) e está dividido nos seguintes tópicos:

* **Épico 1: Qualidade de Código, Padronização e Testes** (Instalação do Ruff, Mypy, pytest e adição de testes unitários/integração).
* **Épico 2: Resiliência, Robustez e Tratamento de Erros** (Migração para `aiokafka` ou `confluent-kafka` e criação de mecanismo de Retry e DLQ).
* **Épico 3: Persistência e Integração com Banco de Dados** (Configuração do PostgreSQL no docker-compose e persistência do estado dos pedidos).
* **Épico 4: Observabilidade e Configuração Dinâmica** (Logs estruturados com structlog, variáveis de ambiente com Pydantic Settings e rota de health check).

Veja todos os detalhes no arquivo [BACKLOG.md](file:///home/work/Documentos/Github/kafka-project/BACKLOG.md).

---

## 👨‍💻 Autor

Projeto desenvolvido para estudo de Kafka, mensageria e arquitetura distribuída.
