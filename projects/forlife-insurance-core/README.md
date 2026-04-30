# Forlife Insurance Core

Biblioteca interna compartilhada pelos projetos `seed`, `api` e `extract`.
Ela centraliza a base técnica e de domínio para evitar duplicação.

## Responsabilidades

- Carregar configurações de banco via variáveis de ambiente.
- Criar engine e sessões SQLAlchemy.
- Declarar a base ORM compartilhada.
- Manter os models relacionais.
- Guardar o ERD em `assets/`.

## Estrutura

```text
src/forlife_insurance_core/
  assets/
  database/
  models/
  config.py
```

## Dependencias

- SQLAlchemy
- python-dotenv
- psycopg2-binary

## Uso Local

```bash
poetry install
```

Os projetos consumidores usam este pacote como dependencia path:

```toml
forlife-insurance-core = { path = "../forlife-insurance-core", develop = true }
```

## Regra de Arquitetura

Este pacote não deve importar código de `forlife-insurance-seed`,
`forlife-insurance-api` ou `forlife-insurance-extract`.
