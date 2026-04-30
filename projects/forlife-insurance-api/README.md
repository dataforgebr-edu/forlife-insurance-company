# Forlife Insurance API

Projeto independente da API transacional do domínio Forlife.

## Responsabilidades

- Expor endpoints HTTP para consumo de aplicações.
- Definir contratos Pydantic ricos para respostas transacionais.
- Consultar os models ORM do `forlife-insurance-core`.
- Manter a camada transacional separada da camada analítica de extract.

## Estrutura

```text
src/forlife_insurance_api/
  app.py
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

## Execucao

```bash
poetry run uvicorn forlife_insurance_api.app:app --reload
```

## Endpoints

```http
GET /apolices
GET /apolices/{apolice_id}
```

## Dependencias

- `forlife-insurance-core`
- FastAPI
- Uvicorn
- Pydantic

## Regra de Arquitetura

Este projeto pode importar `forlife-insurance-core`, mas não deve importar
`forlife-insurance-seed` nem `forlife-insurance-extract`.
