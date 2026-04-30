# Forlife Insurance Extract

Projeto independente de extração analítica do domínio Forlife.

## Responsabilidades

- Expor endpoints HTTP para extração.
- Gerar payloads planos para ingestão em pipelines.
- Suportar extração incremental por `changed_since` e `last_apolice_id`.
- Exportar dados em NDJSON por job CLI.

## Estrutura

```text
src/forlife_insurance_extract/
  app.py
  jobs/
  repositories/
  routers/
  schemas/
  services/
```

## Preparacao

```bash
poetry install
cp .env.example .env
```

Configure o banco:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Executar API de Extract

```bash
poetry run uvicorn forlife_insurance_extract.app:app --reload
```

## Executar Job NDJSON

```bash
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

Parametros opcionais:

```bash
poetry run forlife-extract-apolices \
  --output-path ./out/apolices.ndjson \
  --changed-since 2026-04-01T00:00:00 \
  --last-apolice-id 1000 \
  --limit 5000
```

## Endpoints

```http
GET /extract/apolices
GET /extract/apolices/stream
```

## Dependencias

- `forlife-insurance-core`
- FastAPI
- Uvicorn
- Pydantic

## Regra de Arquitetura

Este projeto pode importar `forlife-insurance-core`, mas não deve importar
`forlife-insurance-api` nem `forlife-insurance-seed`.
