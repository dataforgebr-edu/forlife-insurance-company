# Guia de Desenvolvimento

## Pré-requisitos

- Python >= 3.12 (recomendado: usar [pyenv](https://github.com/pyenv/pyenv))
- [Poetry](https://python-poetry.org/) >= 2.0
- PostgreSQL em execução local ou via Docker

## Estrutura de Ambientes

Este monorepo adota a filosofia de **ambientes independentes por sub-projeto**.
Cada projeto em `projects/` possui seu próprio `pyproject.toml` e virtualenv,
garantindo isolamento de dependências. As ferramentas de qualidade (black,
isort, bandit, pytest, pre-commit) são gerenciadas centralmente na raiz.

## Instalação

### Todos os projetos de uma vez

```bash
# 1. Na raiz: instala as dev deps compartilhadas e o taskipy
poetry install

# 2. Instala todos os sub-projetos
poetry run task install
```

### Projeto específico

```bash
cd projects/forlife-insurance-api
poetry install
```

> **Importante:** instale sempre o `forlife-insurance-core` antes dos projetos
> consumidores, pois eles dependem dele via `path` local.

## Variáveis de Ambiente

Cada projeto possui um `.env.example`. Copie-o antes de executar:

```bash
cp .env.example .env
```

Variáveis obrigatórias:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Comandos Por Projeto

### Seed

```bash
cd projects/forlife-insurance-seed

# Carga única
poetry run forlife-seed --mode once --batch-size 20

# Carga contínua
poetry run forlife-seed --mode continuous --batch-size 20 --interval-seconds 30

# Carga reproduzível
poetry run forlife-seed --mode once --batch-size 20 --seed 42
```

### API

```bash
cd projects/forlife-insurance-api
poetry run uvicorn forlife_insurance_api.app:app --reload
```

### Extract — API

```bash
cd projects/forlife-insurance-extract
poetry run uvicorn forlife_insurance_extract.app:app --reload
```

### Extract — Job CLI

```bash
cd projects/forlife-insurance-extract

# Exportação completa
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson

# Exportação incremental
poetry run forlife-extract-apolices \
  --output-path ./out/apolices.ndjson \
  --changed-since 2026-04-01T00:00:00 \
  --last-apolice-id 1000 \
  --limit 5000
```

## Qualidade de Código

### Via taskipy (todos os projetos)

```bash
poetry run task lint         # formata com black e isort
poetry run task lint-check   # verifica sem alterar arquivos (útil em CI)
poetry run task security     # análise estática com bandit
poetry run task test         # roda pytest
```

### Via poetry run (projeto específico)

```bash
cd projects/forlife-insurance-api
poetry run black src
poetry run isort src
poetry run bandit -r src -lll
poetry run pytest
```

## Pre-commit

Os hooks de qualidade são gerenciados pelo `pre-commit` e configurados na raiz.
Para ativá-los no repositório local:

```bash
# Na raiz do workspace
poetry install         # instala as dev deps compartilhadas
pre-commit install     # registra os hooks no .git
```

A partir daí, `black`, `isort` e `bandit` rodam automaticamente a cada commit.

## Adicionando um Novo Pacote ao Core

1. Crie o model em `projects/forlife-insurance-core/src/forlife_insurance_core/models/`.
2. Registre o re-export em `models/__init__.py` para expor a interface pública:

```python
# models/__init__.py
from forlife_insurance_core.models.novo_model import NovoModel

__all__ = [..., "NovoModel"]
```

3. Faça o mesmo para qualquer novo módulo em `database/` ou `config.py`.

## Adicionando um Novo Sub-projeto

1. Crie a pasta em `projects/forlife-insurance-<nome>/`.
2. Inicialize com `poetry new` ou crie manualmente o `pyproject.toml`.
3. Use `python = ">=3.12,<4.0"` na versão do Python.
4. Adicione a dependência do core se necessário:

```toml
forlife-insurance-core = { path = "../forlife-insurance-core", develop = true }
```

5. **Não** declare dev deps (black, isort, etc.) no `pyproject.toml` do novo projeto — elas já estão na raiz.
6. Adicione o projeto ao `taskipy` na raiz, na variável `PROJECTS`.

## Convenções

- Novas entidades ORM devem entrar em `forlife-insurance-core`.
- Novas rotas transacionais devem entrar em `forlife-insurance-api`.
- Novas extrações analíticas devem entrar em `forlife-insurance-extract`.
- Novas regras de massa fake devem entrar em `forlife-insurance-seed`.
- Evite criar dependências diretas entre `seed`, `api` e `extract`.
- Prefira schemas específicos por interface em vez de reutilizar ORM diretamente.
