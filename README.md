# Forlife Insurance Workspace

Workspace de estudos de engenharia de dados para o domínio de seguros da
Forlife. O código foi organizado em projetos independentes dentro de
`projects/`, cada um com pacote, dependências e entrypoints próprios.

## Projetos

| Projeto | Responsabilidade | Caminho |
| --- | --- | --- |
| Core | Biblioteca compartilhada com configuração, banco, ORM models e ERD. | `projects/forlife-insurance-core` |
| Seed | Geração e carga de dados sintéticos no PostgreSQL. | `projects/forlife-insurance-seed` |
| API | API transacional para consumo de aplicações. | `projects/forlife-insurance-api` |
| Extract | API e job de extração analítica incremental. | `projects/forlife-insurance-extract` |

## Estrutura

```text
forlife-insurance-workspace/
├── pyproject.toml                    # Dev deps compartilhadas (black, isort, bandit, pytest)
├── .pre-commit-config.yaml
├── .python-version
├── docs/
│   ├── architecture.md
│   └── development.md
└── projects/
    ├── forlife-insurance-core/
    │   └── src/forlife_insurance_core/
    ├── forlife-insurance-seed/
    │   └── src/forlife_insurance_seed/
    ├── forlife-insurance-api/
    │   └── src/forlife_insurance_api/
    └── forlife-insurance-extract/
        └── src/forlife_insurance_extract/
```

## Dependências Entre Projetos

```text
forlife-insurance-core
  <- forlife-insurance-seed
  <- forlife-insurance-api
  <- forlife-insurance-extract
```

Boas práticas aplicadas no monorepo:

- O `core` concentra somente código compartilhado de domínio e infraestrutura.
- `seed`, `api` e `extract` dependem do `core` via `path` dependency com `develop = true`.
- Cada projeto possui seu próprio `pyproject.toml` e ambiente virtual independente.
- As ferramentas de qualidade (black, isort, bandit, pytest) são gerenciadas centralmente na raiz.
- Os contratos da API e da extração ficam nos projetos consumidores.
- Os entrypoints CLI ficam declarados apenas nos projetos que os executam.

## Pré-requisitos

- Python >= 3.12
- [Poetry](https://python-poetry.org/) >= 2.0
- PostgreSQL em execução

## Instalação Rápida (todos os projetos)

```bash
# 1. Instala as dev deps e o taskipy na raiz
poetry install

# 2. Instala todos os sub-projetos
poetry run task install
```

Ou projeto a projeto:

```bash
cd projects/forlife-insurance-core && poetry install
cd projects/forlife-insurance-api  && poetry install
```

## Variáveis de Ambiente

Crie um `.env` em cada projeto que for executar, usando o `.env.example` do
próprio projeto como base:

```bash
cp projects/forlife-insurance-api/.env.example projects/forlife-insurance-api/.env
```

Variáveis obrigatórias:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Executar Seed

```bash
cd projects/forlife-insurance-seed
poetry run forlife-seed --mode once --batch-size 20
```

## Executar API

```bash
cd projects/forlife-insurance-api
poetry run uvicorn forlife_insurance_api.app:app --reload
```

## Executar Extract

```bash
cd projects/forlife-insurance-extract
poetry run uvicorn forlife_insurance_extract.app:app --reload

# ou via job CLI:
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

## Comandos Unificados (taskipy)

```bash
poetry run task install      # instala todos os projetos
poetry run task lint         # formata com black e isort em todos os projetos
poetry run task lint-check   # verifica formatação sem alterar arquivos
poetry run task security     # roda bandit em todos os projetos
poetry run task test         # roda pytest em todos os projetos
poetry run task all          # executa install + lint + security + test
```

## Qualidade de Código

As ferramentas de qualidade são configuradas na raiz via `pyproject.toml` e
coordenadas pelo `pre-commit`. Para ativar os hooks localmente:

```bash
poetry install        # na raiz, instala as dev deps compartilhadas
pre-commit install
```

## Documentação

- [Arquitetura](docs/architecture.md)
- [Guia de desenvolvimento](docs/development.md)
- [Core](projects/forlife-insurance-core/README.md)
- [Seed](projects/forlife-insurance-seed/README.md)
- [API](projects/forlife-insurance-api/README.md)
- [Extract](projects/forlife-insurance-extract/README.md)
