# Forlife Insurance API

Projeto independente da API transacional do domínio Forlife.

## Responsabilidades

- Expor endpoints HTTP para consumo de aplicações.
- Definir contratos Pydantic ricos para respostas transacionais.
- Consultar os models ORM do `forlife-insurance-core`.
- Manter a camada transacional separada da camada analítica do `extract`.

## Estrutura

```text
src/forlife_insurance_api/
  app.py
  routers/
    __init__.py
    apolice.py
  schemas/
    __init__.py
    apolice.py
    cliente.py
    corretor.py
    dominios.py
    parcelas.py
    sinistros.py
  services/
    __init__.py
    apolice.py
    parcelas.py
    sinistros.py
```

## Instalação

```bash
cd projects/forlife-insurance-api
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

## Execução

```bash
poetry run uvicorn forlife_insurance_api.app:app --reload
```

## Endpoints

```http
GET /apolices
GET /apolices/{apolice_id}
```

## Dependências

- `forlife-insurance-core` (path local)
- FastAPI >= 0.115
- Uvicorn >= 0.34
- Pydantic >= 2.13
- pydantic-extra-types
- pydantic-br

## Regra de Arquitetura

Este projeto pode importar `forlife-insurance-core`, mas não deve importar
`forlife-insurance-seed` nem `forlife-insurance-extract`.
