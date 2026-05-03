# Forlife Insurance Extract

Projeto independente de extração analítica do domínio Forlife.

## Responsabilidades

- Expor endpoints HTTP para extração de dados.
- Gerar payloads planos e estáveis para ingestão em pipelines.
- Suportar extração incremental por `changed_since` e `last_apolice_id`.
- Exportar dados em NDJSON via job CLI.

## Estrutura

```text
src/forlife_insurance_extract/
  app.py
  jobs/
    __init__.py
    apolice.py      # entrypoint CLI: forlife-extract-apolices
  repositories/
    __init__.py
    apolice.py
  routers/
    __init__.py
    apolice.py
  schemas/
    __init__.py
    apolice.py
  services/
    __init__.py
    apolice.py
```

## Instalação

```bash
cd projects/forlife-insurance-extract
poetry install
cp .env.example .env
```

> O `forlife-insurance-core` é instalado automaticamente como dependência local.

## Variáveis de Ambiente

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
# Exportação completa
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson

# Exportação incremental
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

## Dependências

- `forlife-insurance-core` (path local)
- FastAPI >= 0.115
- Uvicorn >= 0.34
- Pydantic >= 2.13

## Regra de Arquitetura

Este projeto pode importar `forlife-insurance-core`, mas não deve importar
`forlife-insurance-api` nem `forlife-insurance-seed`.
