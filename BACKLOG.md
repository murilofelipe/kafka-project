# 📋 Backlog de Melhorias: kafka-project

Este documento apresenta o planejamento de melhorias e evolução para o projeto **kafka-project** (arquitetura orientada a eventos com Apache Kafka e FastAPI). O objetivo é transformar um protótipo de estudos em um serviço pronto para produção, seguindo as melhores práticas de desenvolvimento, robustez e observabilidade.

---

## 🏛️ Épico 1: Qualidade de Código, Padronização e Testes
**Objetivo:** Garantir a manutenibilidade do projeto por meio de automação de qualidade e testes de software.

### 🎫 Story 1.1: Configuração de Ferramentas de Qualidade Estática
- **Descrição:** Como desenvolvedor, quero que o código seja formatado e validado automaticamente para seguir os padrões da comunidade PEP 8.
- **Tarefas:**
  - [ ] Adicionar um arquivo `.gitignore` adequado para projetos Python (evitando commits de `__pycache__`, arquivos de IDE, etc.).
  - [ ] Configurar `ruff` (linter e formatador super rápido) para unificar a formatação e linting.
  - [ ] Adicionar validações de tipagem estática com `mypy`.
  - [ ] Atualizar o `Makefile` com o comando `make lint` e `make format`.

### 🎫 Story 1.2: Implementação de Testes Automatizados (Unitários e Integração)
- **Descrição:** Como desenvolvedor, quero rodar testes para garantir que alterações no código não causem regressões.
- **Tarefas:**
  - [ ] Instalar e configurar `pytest` no projeto.
  - [ ] Desenvolver testes unitários para os endpoints da API (FastAPI) utilizando `FastAPI.testclient`.
  - [ ] Desenvolver testes unitários para as funções utilitárias de conexão do Kafka.
  - [ ] Implementar testes de integração simulando o broker Kafka (utilizando mocks ou o pacote `testcontainers`).
  - [ ] Adicionar o comando `make test` ao `Makefile`.

---

## 🛡️ Épico 2: Resiliência, Robustez e Tratamento de Erros
**Objetivo:** Evitar perda de mensagens e garantir que o processamento de eventos seja resiliente a falhas temporárias ou definitivas.

### 🎫 Story 2.1: Migração para Biblioteca Kafka Atualizada
- **Descrição:** Como arquiteto, quero migrar da biblioteca desatualizada `kafka-python` para `aiokafka` (assíncrona) ou `confluent-kafka` (performática e mantida oficialmente).
- **Tarefas:**
  - [ ] Avaliar a viabilidade e escolher entre `aiokafka` (assíncrona native-FastAPI) e `confluent-kafka`.
  - [ ] Substituir `kafka-python` na dependência e refatorar `src/core/kafka_config.py`.
  - [ ] Atualizar o código do Producer em `src/api/main.py` e do Consumer em `src/consumer/worker.py`.

### 🎫 Story 2.2: Implementação de Retry e Dead Letter Queue (DLQ)
- **Descrição:** Como operador do sistema, quero que mensagens que falhem no processamento sejam reprocessadas e, em caso de erro persistente, enviadas para uma fila de erros (DLQ).
- **Tarefas:**
  - [ ] Configurar uma política de retentativas (Retry Pattern) com backoff exponencial no Consumer.
  - [ ] Definir o tópico `pedidos-dlq` no script de criação de tópicos.
  - [ ] Implementar a lógica de direcionamento para a DLQ no Consumer caso o processamento de um pedido falhe após $N$ tentativas.

---

## 💾 Épico 3: Persistência e Integração com Banco de Dados
**Objetivo:** Sair do modelo em memória e persistir o estado dos pedidos para consulta e consistência de dados.

### 🎫 Story 3.1: Configuração do Banco de Dados Relacional
- **Descrição:** Como desenvolvedor, quero adicionar um contêiner PostgreSQL no Docker Compose para salvar os dados da aplicação.
- **Tarefas:**
  - [ ] Atualizar o `docker-compose.yml` adicionando o serviço do banco de dados (PostgreSQL).
  - [ ] Adicionar suporte a ORM (`SQLAlchemy` ou `SQLModel`) no `requirements.txt`.
  - [ ] Configurar la conexão do banco de dados na inicialização da aplicação FastAPI.

### 🎫 Story 3.2: Persistência do Estado do Pedido
- **Descrição:** Como usuário do sistema, quero que meu pedido seja gravado no banco de dados com o status correspondente.
- **Tarefas:**
  - [ ] Criar a tabela `pedidos` com campos `id`, `status`, `criado_em`, `atualizado_em`.
  - [ ] Modificar o endpoint `POST /pedido` para salvar o pedido no banco com status `PENDENTE` antes de publicar o evento.
  - [ ] Modificar o Consumer para atualizar o status do pedido no banco para `PAGO` ou `FALHADO` após o processamento.

---

## 📈 Épico 4: Observabilidade e Configuração Dinâmica
**Objetivo:** Permitir monitorar a saúde do sistema e configurar os recursos sem alterar o código-fonte.

### 🎫 Story 4.1: Configuração Dinâmica com Pydantic Settings
- **Descrição:** Como engenheiro de DevOps, quero configurar variáveis como brokers, tópicos e credenciais via variáveis de ambiente usando Pydantic Settings.
- **Tarefas:**
  - [ ] Adicionar a biblioteca `pydantic-settings` ao projeto.
  - [ ] Criar a classe `Settings` em `src/core/config.py`.
  - [ ] Substituir chamadas de `os.getenv` por referências ao objeto global `settings`.

### 🎫 Story 4.2: Logs Estruturados e Observabilidade
- **Descrição:** Como operador do sistema, quero ver logs estruturados em formato JSON para facilitar a busca em ferramentas de agregação de logs (Elasticsearch/Splunk).
- **Tarefas:**
  - [ ] Substituir o uso de `print` no produtor e consumidor pela biblioteca padrão `logging` estruturada ou `structlog`.
  - [ ] Adicionar metadados cruciais aos logs (como `pedido_id` e tempo de execução do processamento).
  - [ ] Implementar um endpoint de Health Check `/health` na API FastAPI que teste a conectividade com o Kafka e com o banco de dados.
