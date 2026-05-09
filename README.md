# Forlife Insurance Company

Monorepo de portfólio para o domínio de seguros de vida. Quatro pacotes Python convivem em um único ambiente virtual gerenciado pelo Poetry a partir da raiz.

## Pacotes

| Pacote | Responsabilidade |
|---|---|
| `forlife_insurance_core` | Biblioteca compartilhada: ORM models, configuração de banco, session management |
| `forlife_insurance_api` | FastAPI transacional — CRUD de apólices, clientes, corretores, sinistros e parcelas |
| `forlife_insurance_seed` | Gerador Faker para seed sintético do PostgreSQL |
| `forlife_insurance_ui` | Dashboard Streamlit para visualização dos dados |

Hierarquia de dependência: **Core ← API, Seed** (UI acessa a API via HTTP).

## Estrutura

```
forlife-insurance-company/
├── pyproject.toml          # único — consolida todas as dependências e tasks
├── poetry.lock
├── .env                    # variáveis de conexão com o banco
├── .python-version
├── .pre-commit-config.yaml
└── projects/
    ├── forlife_insurance_core/
    │   ├── config.py
    │   ├── database/
    │   └── models/
    ├── forlife_insurance_api/
    │   ├── app.py
    │   ├── routers/
    │   ├── schemas/
    │   └── services/
    ├── forlife_insurance_seed/
    │   ├── runner.py
    │   ├── bootstrap.py
    │   └── factories.py
    └── forlife_insurance_ui/
        ├── app.py
        ├── pages/
        └── services/
```

## Pré-requisitos

- Python 3.12 (gerenciado via `.python-version`)
- [Poetry](https://python-poetry.org/) >= 2.0
- PostgreSQL em execução

## Instalação

```bash
# Clona e instala tudo de uma vez
git clone <repo-url>
cd forlife-insurance-company
poetry install
```

## Variáveis de Ambiente

Crie um `.env` na raiz com as credenciais do PostgreSQL:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Executar os Serviços

```bash
# API transacional (FastAPI)
poetry run task api

# Interface web (Streamlit)
poetry run task ui

# Seed do banco (carga única de dados sintéticos)
poetry run task seed
```

Por padrão a API sobe em `http://localhost:8000` e a UI em `http://localhost:8501`.

## Comandos de Qualidade

```bash
poetry run task lint         # formata código com black + isort
poetry run task lint-check   # verifica formatação sem alterar arquivos (CI)
poetry run task security     # análise estática com bandit
poetry run task test         # roda pytest
```

## Pre-commit

```bash
poetry install
pre-commit install
```

Os hooks rodam black, isort e bandit automaticamente a cada `git commit`.
