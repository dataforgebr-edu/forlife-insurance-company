# Seed App

Aplicativo responsavel por criar e popular a base PostgreSQL com dados
sinteticos coerentes com as regras de negocio da seguradora.

Este README cobre apenas o fluxo de seed. Para a visao geral do repositorio,
consulte [README.md](../../README.md).

## Objetivo

Gerar uma base relacional para estudos de modelagem, engenharia de dados,
qualidade de dados e consumo analitico, preservando coerencia entre clientes,
corretores, apolices, parcelas e sinistros.

## Codigo Relacionado

O seed esta implementado em `src/forlife_insurance/seed`.

Principais modulos:

- `bootstrap.py`: carga inicial das tabelas de dominio.
- `factories.py`: geracao de dados sinteticos.
- `runner.py`: orquestracao da execucao do seed.
- `types.py`: estruturas auxiliares para o fluxo de carga.

## Requisitos

- Pyenv `3.x`
- Python `3.14.2`
- Poetry `2.x`
- PostgreSQL disponivel localmente ou em container

## Preparacao do Ambiente

Defina a versao local do Python:

```bash
pyenv local 3.14.2
```

Instale as dependencias:

```bash
poetry install
```

Crie o arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Preencha as variaveis:

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

As tabelas sao criadas automaticamente durante a execucao do seed.

## Como Executar

Comando principal:

```bash
poetry run forlife-seed
```

Execucao unica:

```bash
poetry run forlife-seed --mode once --batch-size 20
```

Execucao continua:

```bash
poetry run forlife-seed --mode continuous --batch-size 20 --interval-seconds 30
```

Execucao reproduzivel:

```bash
poetry run forlife-seed --mode once --batch-size 20 --seed 42
```

## Regras de Negocio

- As tabelas de dominio sao carregadas na primeira execucao.
- Antes de uma venda de apolice, deve existir um corretor cadastrado.
- Antes de uma venda de apolice, deve existir um cliente cadastrado.
- Toda apolice possui cliente, corretor, produto, periodicidade, status e meio
  de pagamento.
- A data de inicio de vigencia da apolice respeita a existencia previa do
  cliente e do corretor.
- Um cliente pode ter uma ou varias apolices.
- Um corretor pode vender nenhuma, uma ou varias apolices.
- As parcelas sao geradas dentro do periodo de vigencia da apolice.
- Nem toda apolice possui sinistro.

## Modelo ERD

O diagrama-fonte do modelo relacional utilizado pelo seed esta em:

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
    DATE data_nascimento
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
    INTEGER status_apolice_id FK
  }

  parcela {
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

  sinistro {
    INTEGER sinistro_id PK
    FLOAT valor
    DATETIME data_pagamento
    DATETIME data_insercao
    DATETIME data_atualizacao
    INTEGER status_sinistro_id FK
    INTEGER meio_pagamento_id FK
    INTEGER apolice_id FK
  }

  estado {
    INTEGER estado_id PK
    VARCHAR uf
    VARCHAR descricao
  }

  cidade {
    INTEGER cidade_id PK
    VARCHAR descricao
    INTEGER estado_id FK
  }

  produto {
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

  status_apolice {
    INTEGER status_apolice_id PK
    VARCHAR descricao
  }

  status_sinistro {
    INTEGER status_sinistro_id PK
    VARCHAR descricao
  }

  estado ||--o{ cidade : possui
  cidade ||--o{ cliente : localiza
  estado ||--o{ corretor : habilita

  cliente ||--o{ apolice : contrata
  corretor ||--o{ apolice : vende
  produto ||--o{ apolice : classifica
  periodicidade_pagamento ||--o{ apolice : define
  meio_pagamento ||--o{ apolice : cobra
  status_apolice ||--o{ apolice : status

  apolice ||--o{ parcela : gera
  meio_pagamento ||--o{ parcela : quita

  apolice ||--o{ sinistro : origina
  meio_pagamento ||--o{ sinistro : paga
  status_sinistro ||--o{ sinistro : status
```

## Comandos Uteis

Formatacao:

```bash
poetry run black src
poetry run isort src
```

Analise de seguranca:

```bash
poetry run bandit -r src -lll
```

Pre-commit:

```bash
poetry run pre-commit install
poetry run pre-commit run --all-files
```
