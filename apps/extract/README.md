# Extract App

Aplicativo responsável por expor e executar extrações analíticas do domínio,
pensadas para consumo por pipeline de data lake.

Este README cobre apenas o fluxo de extração. Para a visão geral do repositório,
consulte [README.md](../../README.md).

## Objetivo

Fornecer uma camada separada da API transacional para extração de dados em
formato plano, incremental e orientado a ingestão analítica.

O foco aqui é:

- consultas explícitas com projeção de colunas;
- extração incremental por `data_atualizacao` e chave incremental;
- payloads estáveis para carga em data lake;
- consumo por API dedicada ou por job em lote.

## Código Relacionado

A implementação da camada de extração está em `src/forlife_insurance/extract`.

Principais módulos:

- `app.py`: aplicação FastAPI dedicada à extração.
- `routers/`: endpoints HTTP de extração.
- `repositories/`: consultas SQLAlchemy voltadas à leitura analítica.
- `schemas/`: modelos planos para serialização e ingestão.
- `services/`: orquestração da extração.
- `jobs/`: jobs de exportação para arquivos e pipelines.

## Endpoints

A aplicação expõe atualmente a extração de apólices.

### Listagem em lote

```http
GET /extract/apolices
```

Parâmetros aceitos:

- `changed_since`: filtra registros alterados depois da data informada;
- `last_apolice_id`: permite paginação incremental por chave;
- `limit`: limita a quantidade de linhas retornadas.

### Streaming NDJSON

```http
GET /extract/apolices/stream
```

Esse endpoint retorna uma linha JSON por registro, no formato NDJSON, o que é
útil para pipelines que preferem consumo em streaming.

## Job de Exportação

Além do endpoint HTTP, existe um job CLI para exportar apólices em arquivo
NDJSON.

Comando:

```bash
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

Parâmetros úteis:

- `--changed-since 2026-04-01T00:00:00`
- `--last-apolice-id 1000`
- `--limit 5000`

Exemplo:

```bash
poetry run forlife-extract-apolices \
  --output-path ./out/apolices.ndjson \
  --changed-since 2026-04-01T00:00:00 \
  --limit 10000
```

## Requisitos

- Pyenv `3.x`
- Python `3.14.2`
- Poetry `2.x`
- PostgreSQL disponível localmente ou em container

## Preparação do Ambiente

Defina a versão local do Python:

```bash
pyenv local 3.14.2
```

Instale as dependências:

```bash
poetry install
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis de banco:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Como Executar

Subir a API de extração:

```bash
poetry run uvicorn forlife_insurance.extract.app:app --reload
```

Executar o job de exportação:

```bash
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

## Observações de Arquitetura

- A camada `extract` é separada da API transacional.
- Os schemas de extração são planos e orientados a ingestão.
- O consumo ideal aqui é incremental e com paginação por cursor ou watermark.
- A mesma lógica de consulta é reutilizada entre endpoint HTTP e job CLI.

