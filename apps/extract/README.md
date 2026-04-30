# Extract App

Aplicativo responsavel por expor extracoes analiticas do dominio, pensadas para
consumo por pipeline de data lake e jobs de ingestao.

Este README cobre apenas o fluxo de extracao. Para a visao geral do repositorio,
consulte [README.md](../../README.md).

## Objetivo

Fornecer uma camada separada da API transacional para extracao de dados em
formato plano, incremental e orientado a ingestao analitica.

O foco aqui e:

- consultas explicitamente projetadas com poucas colunas;
- extracao incremental por `data_atualizacao` e chave incremental;
- payloads estaveis para carga em lake ou stage;
- consumo por API dedicada ou por job em lote.

## Codigo Relacionado

A implementacao da camada de extracao esta em `src/forlife_insurance/extract`.

Principais modulos:

- `app.py`: aplicacao FastAPI dedicada a extracao.
- `routers/`: endpoints HTTP de extracao.
- `repositories/`: consultas SQLAlchemy voltadas a leitura analitica.
- `schemas/`: modelos planos para serializacao e ingestao.
- `services/`: orquestracao da extracao.
- `jobs/`: jobs de exportacao para arquivos e pipelines.

## Endpoints

A aplicacao expoe atualmente a extracao de apolices.

### Listagem em lote

```http
GET /extract/apolices
```

Parametros aceitos:

- `changed_since`: filtra registros alterados depois da data informada;
- `last_apolice_id`: permite paginacao incremental por chave;
- `limit`: limita a quantidade de linhas retornadas.

### Streaming NDJSON

```http
GET /extract/apolices/stream
```

Esse endpoint retorna uma linha JSON por registro, no formato NDJSON, util
para pipelines que preferem consumo em streaming.

## Job de Exportacao

Alem do endpoint HTTP, existe um job CLI para exportar apolices em arquivo
NDJSON.

Comando:

```bash
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

Parametros uteis:

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
- PostgreSQL disponivel localmente ou em container

## Preparacao do Ambiente

Defina a versao local do Python:

```bash
pyenv local 3.14.2
```

Instale as dependencias:

```bash
poetry install
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variaveis de banco:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Como Executar

Subir a API de extracao:

```bash
poetry run uvicorn forlife_insurance.extract.app:app --reload
```

Executar o job de exportacao:

```bash
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

## Observacoes de Arquitetura

- A camada `extract` e separada da API transacional.
- Os schemas de extracao sao planos e orientados a ingestao.
- O consumo ideal aqui e incremental e com paginacao por cursor ou watermark.
- A mesma logica de consulta e reutilizada entre endpoint HTTP e job CLI.
