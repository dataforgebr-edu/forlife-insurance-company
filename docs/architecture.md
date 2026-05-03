# Arquitetura

## Visão Geral

O repositório foi separado em projetos independentes para reduzir acoplamento e
preparar a evolução para pipelines, orquestração e camadas analíticas.

```text
PostgreSQL
  ^
  |
forlife-insurance-core
  |-- database/ (engine, sessões, Base ORM)
  |-- models/ (entidades relacionais)
  |-- config.py (variáveis de ambiente)
  |-- assets/ (ERD)
  |
  ├── forlife-insurance-seed    (carga de dados sintéticos)
  ├── forlife-insurance-api     (API transacional)
  └── forlife-insurance-extract (API e job analítico)
```

## Filosofia de Monorepo

Este projeto adota a filosofia de **ambientes independentes por sub-projeto**:

- Cada projeto possui seu próprio `pyproject.toml` e virtualenv.
- A dependência entre projetos é declarada via `path` do Poetry com `develop = true`.
- As ferramentas de qualidade são centralizadas no `pyproject.toml` da raiz.
- A orquestração de comandos (install, lint, test) é feita pelo `taskipy` na raiz.

Essa abordagem garante isolamento de dependências, ciclos de deploy independentes
e clareza sobre o que cada projeto precisa para funcionar.

## Fronteiras

### Core

Biblioteca interna compartilhada. Deve conter apenas recursos que todos os
projetos podem utilizar sem criar dependência circular.

Responsabilidades:

- leitura de variáveis de ambiente;
- criação de engine e sessões SQLAlchemy;
- base declarativa ORM;
- modelos ORM;
- assets compartilhados, como o ERD.

Interface pública (re-exportada via `__init__.py`):

```python
from forlife_insurance_core.models import Apolice, Cliente, Corretor
from forlife_insurance_core.database import Base, get_db, session_scope
```

Não deve conter:

- rotas HTTP;
- jobs específicos;
- schemas Pydantic de API ou extract;
- lógica de geração de dados fake.

### Seed

Projeto responsável por criar massa sintética coerente para o banco
transacional.

Responsabilidades:

- carregar tabelas de domínio;
- gerar clientes, corretores, apólices, parcelas e sinistros;
- executar em modo pontual ou contínuo;
- usar `forlife-insurance-core` como fonte de models e banco.

Entrypoint CLI declarado em `pyproject.toml`:

```toml
[tool.poetry.scripts]
forlife-seed = "forlife_insurance_seed.runner:main"
```

### API

Projeto responsável por expor dados para consumo transacional de aplicações.

Responsabilidades:

- rotas FastAPI;
- schemas Pydantic ricos e navegáveis;
- services de consulta voltados a produto;
- tratamento de erros HTTP.

### Extract

Projeto responsável por expor dados para consumo analítico e pipelines.

Responsabilidades:

- rotas FastAPI de extração;
- schemas planos e estáveis;
- consultas incrementais por watermark e chave;
- job CLI para exportação NDJSON.

Entrypoint CLI declarado em `pyproject.toml`:

```toml
[tool.poetry.scripts]
forlife-extract-apolices = "forlife_insurance_extract.jobs.apolice:main"
```

## Regras de Dependência

- `core` não importa `seed`, `api` nem `extract`.
- `seed`, `api` e `extract` podem importar `core`.
- `api` não importa `extract`.
- `extract` não importa `api`.
- `seed` não importa `api` nem `extract`.
- Projetos novos devem ser criados dentro de `projects/`.
- Dev deps (black, isort, bandit, pytest) não devem ser declaradas nos sub-projetos — ficam apenas na raiz.

## Gerenciamento de Dependências

Cada sub-projeto referencia o `core` via dependência de path local:

```toml
# Em qualquer sub-projeto
[tool.poetry.dependencies]
forlife-insurance-core = { path = "../forlife-insurance-core", develop = true }
```

O `develop = true` garante que alterações no `core` são refletidas
imediatamente nos consumidores sem precisar reinstalar.

## Orquestração (taskipy)

O `taskipy` na raiz coordena operações em todos os projetos via `poetry run task <comando>`:

```bash
poetry run task install      # poetry install em todos os projetos
poetry run task lint         # black + isort em todos os projetos
poetry run task lint-check   # verificação de lint sem alterar arquivos (CI)
poetry run task security     # bandit em todos os projetos
poetry run task test         # pytest em todos os projetos
poetry run task all          # install + lint + security + test
```

## Evolução Recomendada

1. Criar testes por projeto com pytest e fixtures compartilhadas.
2. Adicionar CI (GitHub Actions) com os alvos `lint-check`, `security` e `test`.
3. Criar contratos de dados formais para o `extract` (ex: JSON Schema ou Pandera).
4. Integrar o `extract` a um orquestrador como Airflow ou Prefect.
5. Evoluir a saída analítica para camadas raw, silver e gold.
6. Publicar o `core` em um registry privado (PyPI interno ou GitHub Packages)
   quando o número de consumidores crescer.
