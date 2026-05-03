# Forlife Insurance Core

Biblioteca interna compartilhada pelos projetos `seed`, `api` e `extract`.
Centraliza a base técnica e de domínio para evitar duplicação entre os
consumidores.

## Responsabilidades

- Carregar configurações de banco via variáveis de ambiente.
- Criar engine e sessões SQLAlchemy.
- Declarar a base ORM compartilhada (`Base`).
- Manter os models relacionais.
- Guardar o ERD em `assets/`.

## Estrutura

```text
src/forlife_insurance_core/
  assets/
    database_diagrama.erd.json
  database/
    __init__.py     # re-exporta Base, get_db, session_scope, init_database
    database.py
  models/
    __init__.py     # re-exporta todos os models (Apolice, Cliente, etc.)
    apolice.py
    cliente.py
    corretor.py
    dominios.py
    parcelas.py
    sinistros.py
  config.py
  __init__.py
```

## Instalação

```bash
cd projects/forlife-insurance-core
poetry install
cp .env.example .env
```

## Uso nos Projetos Consumidores

Declare como dependência local no `pyproject.toml` do sub-projeto:

```toml
[tool.poetry.dependencies]
forlife-insurance-core = { path = "../forlife-insurance-core", develop = true }
```

O `develop = true` garante que alterações no `core` são refletidas
imediatamente sem reinstalação.

### Importando Models

```python
# Via interface pública (recomendado)
from forlife_insurance_core.models import Apolice, Cliente, Corretor

# Via módulo direto (quando necessário)
from forlife_insurance_core.models.dominios import StatusApolice
```

### Importando Database

```python
from forlife_insurance_core.database import Base, get_db, session_scope, init_database
```

## Variáveis de Ambiente

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Dependências

- SQLAlchemy >= 2.0
- python-dotenv
- psycopg2-binary

## Regra de Arquitetura

Este pacote não deve importar código de `forlife-insurance-seed`,
`forlife-insurance-api` ou `forlife-insurance-extract`.
