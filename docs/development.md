# Guia de Desenvolvimento

## Ambiente

Cada projeto em `projects/` possui seu próprio `pyproject.toml`. Para trabalhar
em um projeto específico, entre na pasta dele e execute `poetry install`.

Exemplo:

```bash
cd projects/forlife-insurance-api
poetry install
```

## Variáveis de Ambiente

Copie o `.env.example` do projeto que será executado:

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

Seed:

```bash
cd projects/forlife-insurance-seed
poetry run forlife-seed --mode once --batch-size 20
```

API:

```bash
cd projects/forlife-insurance-api
poetry run uvicorn forlife_insurance_api.app:app --reload
```

Extract API:

```bash
cd projects/forlife-insurance-extract
poetry run uvicorn forlife_insurance_extract.app:app --reload
```

Extract job:

```bash
cd projects/forlife-insurance-extract
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

## Qualidade

Execute os comandos dentro do projeto alterado:

```bash
poetry run black src
poetry run isort src
poetry run bandit -r src -lll
poetry run pytest
```

## Convencoes

- Novas entidades ORM devem entrar em `forlife-insurance-core`.
- Novas rotas transacionais devem entrar em `forlife-insurance-api`.
- Novas extrações analíticas devem entrar em `forlife-insurance-extract`.
- Novas regras de massa fake devem entrar em `forlife-insurance-seed`.
- Evite criar dependências diretas entre `seed`, `api` e `extract`.
- Prefira schemas especificos por interface em vez de reutilizar ORM diretamente.
