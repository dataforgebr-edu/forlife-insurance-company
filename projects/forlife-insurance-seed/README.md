# Forlife Insurance Seed

Projeto independente responsável por popular o PostgreSQL com dados sintéticos
coerentes para o domínio de seguros.

## Responsabilidades

- Carregar tabelas de domínio.
- Gerar clientes, corretores, apólices, parcelas e sinistros.
- Executar carga unica ou continua.
- Consumir models e sessões do `forlife-insurance-core`.

## Estrutura

```text
src/forlife_insurance_seed/
  bootstrap.py
  factories.py
  runner.py
  types.py
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

Carga unica:

```bash
poetry run forlife-seed --mode once --batch-size 20
```

Carga continua:

```bash
poetry run forlife-seed --mode continuous --batch-size 20 --interval-seconds 30
```

Carga reproduzivel:

```bash
poetry run forlife-seed --mode once --batch-size 20 --seed 42
```

## Dependencias

- `forlife-insurance-core`
- Faker

## Observacoes

As tabelas são criadas automaticamente pelo fluxo de seed usando os models do
core. O banco PostgreSQL definido em `DB_NAME` precisa existir antes da
execução.
