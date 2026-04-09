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

## 🚀 Próximos passos (roadmap)

- [ ] Criar evento `pedido.pago`
- [ ] Criar segundo consumer (envio/logística)
- [ ] Persistência com banco de dados (PostgreSQL)
- [ ] Implementar retry e DLQ (Dead Letter Queue)
- [ ] Adicionar observabilidade (logs estruturados / tracing)

---

## 👨‍💻 Autor

Projeto desenvolvido para estudo de Kafka, mensageria e arquitetura distribuída.
