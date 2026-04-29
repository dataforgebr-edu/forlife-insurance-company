# Seed App

Aplicativo responsável por criar e popular a base PostgreSQL com dados
sintéticos coerentes com as regras de negócio da seguradora.

Este README cobre apenas o fluxo de seed. Para a visão geral do repositório,
consulte [README.md](../../README.md).

## Objetivo

Gerar uma base relacional para estudos de modelagem, engenharia de dados,
qualidade de dados e consumo analítico, preservando coerência entre clientes,
corretores, apólices, parcelas e sinistros.

## Código Relacionado

O seed está implementado em `src/forlife_insurance/seed`.

Principais módulos:

- `bootstrap.py`: carga inicial das tabelas de domínio.
- `factories.py`: geração de dados sintéticos.
- `runner.py`: orquestração da execução do seed.
- `types.py`: estruturas auxiliares para o fluxo de carga.

## Requisitos

- Pyenv `3.x`
- Python `3.14.2`
- Poetry `2.x`
- PostgreSQL disponível localmente ou em container

## Preparação do Ambiente

Defina a versão local do Python:

```bash
pyenv local 3.14.2
```

Instale as dependências:

```bash
poetry install
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variáveis:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Banco de Dados

Crie previamente um banco PostgreSQL com o nome definido em `DB_NAME`.

Exemplo:

```bash
createdb seguros
```

Ou:

```bash
psql -U postgres -c "CREATE DATABASE seguros;"
```

As tabelas são criadas automaticamente durante a execução do seed.

## Como Executar

Comando principal:

```bash
poetry run forlife-seed
```

Execução única:

```bash
poetry run forlife-seed --mode once --batch-size 20
```

Execução contínua:

```bash
poetry run forlife-seed --mode continuous --batch-size 20 --interval-seconds 30
```

Execução reproduzível:

```bash
poetry run forlife-seed --mode once --batch-size 20 --seed 42
```

## Regras de Negócio

- As tabelas de domínio são carregadas na primeira execução.
- Antes de uma venda de apólice, deve existir um corretor cadastrado.
- Antes de uma venda de apólice, deve existir um cliente cadastrado.
- Toda apólice possui cliente, corretor, produto, periodicidade e meio de
  pagamento.
- A data de início de vigência da apólice respeita a existência prévia do
  cliente e do corretor.
- Um cliente pode ter uma ou várias apólices.
- Um corretor pode vender nenhuma, uma ou várias apólices.
- As parcelas são geradas dentro do período de vigência da apólice.
- Nem toda apólice possui sinistro.

## Modelo ERD

O diagrama-fonte do modelo relacional utilizado pelo seed está em:

```text
src/forlife_insurance/assets/database_diagrama.erd.json
```

O desenho abaixo mostra as tabelas e os relacionamentos entre elas:

```mermaid
erDiagram
  cliente {
    INTEGER cliente_id PK
    VARCHAR nome
    VARCHAR email
    VARCHAR telefone
    VARCHAR endereco
    DATETIME data_nascimento
    DATETIME data_insercao
    DATETIME data_atualizacao
    INTEGER cidade_id FK
  }

  corretor {
    INTEGER corretor_id PK
    VARCHAR nome
    VARCHAR cnpj
    VARCHAR email
    DATETIME data_insercao
    DATETIME data_atualizacao
    INTEGER estado_id FK
  }

  apolice {
    INTEGER apolice_id PK
    FLOAT capital_segurado
    FLOAT premio
    DATETIME inicio_vigencia
    DATETIME fim_vigencia
    DATETIME data_insercao
    DATETIME data_atualizacao
    INTEGER periodicidade_id FK
    INTEGER produto_id FK
    INTEGER corretor_id FK
    INTEGER cliente_id FK
    INTEGER meio_pagamento_id FK
    INTEGER estatus_apolice_id FK
  }

  parcelas {
    INTEGER parcela_id PK
    FLOAT valor
    DATETIME data_emissao
    DATETIME data_periodo
    DATETIME data_pagamento
    DATETIME data_insercao
    DATETIME data_atualizacao
    INTEGER meio_pagamento_id FK
    INTEGER apolice_id FK
  }

  sinistros {
    INTEGER sinistro_id PK
    FLOAT valor
    DATETIME data_pagamento
    DATETIME data_insercao
    DATETIME data_atualizacao
    INTEGER estatus_sinistro_id FK
    INTEGER meio_pagamento_id FK
    INTEGER apolice_id FK
  }

  estados {
    INTEGER estado_id PK
    VARCHAR uf
    VARCHAR descricao
  }

  cidades {
    INTEGER cidade_id PK
    VARCHAR descricao
    INTEGER estado_id FK
  }

  produtos {
    INTEGER produto_id PK
    VARCHAR descricao
  }

  periodicidade_pagamento {
    INTEGER periodicidade_id PK
    VARCHAR descricao
  }

  meio_pagamento {
    INTEGER meio_pagamento_id PK
    VARCHAR descricao
  }

  estatus_apolice {
    INTEGER estatus_apolice_id PK
    VARCHAR descricao
  }

  estatus_sinistro {
    INTEGER estatus_sinistro_id PK
    VARCHAR descricao
  }

  estados ||--o{ cidades : possui
  cidades ||--o{ cliente : localiza
  estados ||--o{ corretor : habilita

  cliente ||--o{ apolice : contrata
  corretor ||--o{ apolice : vende
  produtos ||--o{ apolice : classifica
  periodicidade_pagamento ||--o{ apolice : define
  meio_pagamento ||--o{ apolice : cobra
  estatus_apolice ||--o{ apolice : status

  apolice ||--o{ parcelas : gera
  meio_pagamento ||--o{ parcelas : quita

  apolice ||--o{ sinistros : origina
  meio_pagamento ||--o{ sinistros : paga
  estatus_sinistro ||--o{ sinistros : status
```

## Comandos Úteis

Formatação:

```bash
poetry run black src
poetry run isort src
```

Análise de segurança:

```bash
poetry run bandit -r src -lll
```

Pre-commit:

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```
