# Forlife Insurance Seed

Projeto independente responsável por popular o PostgreSQL com dados sintéticos
coerentes para o domínio de seguros.

## Responsabilidades

- Carregar tabelas de domínio (cidades, estados, produtos, etc.).
- Gerar clientes, corretores, apólices, parcelas e sinistros via Faker.
- Executar carga única ou contínua.
- Consumir models e sessões do `forlife-insurance-core`.

## Estrutura

```text
src/forlife_insurance_seed/
  bootstrap.py    # carga das tabelas de domínio
  factories.py    # geração de entidades com Faker
  runner.py       # entrypoint CLI: forlife-seed
  types.py        # tipos internos do seed
```

## Instalação

```bash
cd projects/forlife-insurance-seed
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

> O banco definido em `DB_NAME` precisa existir antes da execução. As tabelas
> são criadas automaticamente pelo seed via os models do core.

## Execução

```bash
# Carga única (20 registros por entidade)
poetry run forlife-seed --mode once --batch-size 20

# Carga contínua (a cada 30 segundos)
poetry run forlife-seed --mode continuous --batch-size 20 --interval-seconds 30

# Carga reproduzível (seed fixo para testes)
poetry run forlife-seed --mode once --batch-size 20 --seed 42
```

## Dependências

- `forlife-insurance-core` (path local)
- Faker >= 37.11

## Regra de Arquitetura

Este projeto pode importar `forlife-insurance-core`, mas não deve importar
`forlife-insurance-api` nem `forlife-insurance-extract`.
