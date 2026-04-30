# Forlife Insurance Company

Projeto de dados para uma seguradora que vende apolices nos segmentos de vida,
automovel e residencia.

O repositorio concentra a base transacional do dominio e os aplicativos que
operam sobre ela. Hoje o foco esta em tres fluxos principais:

- geracao de dados sinteticos coerentes com as regras de negocio da seguradora;
- exposicao desses dados por meio de uma API transacional;
- extracao incremental para consumo analitico e jobs de ingestao.

## Visao Geral

O projeto foi organizado como um monorepo simples com um pacote Python
compartilhado e documentacao separada por aplicativo.

- `seed`: cria e popula a base PostgreSQL com dados sinteticos.
- `api`: expõe os dados do projeto para consumo por aplicacoes, estudos e
  integracoes.
- `extract`: disponibiliza consultas planas e incrementais para pipeline e
  data lake.

Os tres apps compartilham os mesmos modulos de dominio, conexao com banco e
modelos relacionais, evitando duplicacao de regras e mantendo uma unica fonte
de verdade para a estrutura dos dados.

## Estrutura

```text
forlife-insurance-company/
  README.md
  pyproject.toml
  poetry.lock
  .env.example

  apps/
    seed/
      README.md
    api/
      README.md
    extract/
      README.md

  src/
    forlife_insurance/
      core/
      database/
      models/
      seed/
      extract/
      assets/
```

## Package Python

O codigo compartilhado fica em `src/forlife_insurance`.

- `core/`: configuracao da aplicacao e leitura de variaveis de ambiente.
- `database/`: engine, sessoes e base do SQLAlchemy.
- `models/`: definicao das tabelas e relacionamentos.
- `seed/`: implementacao do processo de carga sintetica.
- `extract/`: implementacao da camada de extracao analitica e dos jobs de
  exportacao.
- `assets/`: artefatos de apoio, incluindo o diagrama ERD.

## Aplicativos

### Seed

Responsavel por criar a estrutura relacional e popular o banco com dados
sinteticos consistentes com o dominio de seguros.

Documentacao: [apps/seed/README.md](apps/seed/README.md)

### API

Responsavel por expor os dados do projeto por HTTP, reaproveitando os modelos e
modulos compartilhados do pacote principal.

Documentacao: [apps/api/README.md](apps/api/README.md)

### Extract

Responsavel por expor consultas planas, streaming NDJSON e jobs CLI para
consumo analitico e orquestracao.

Documentacao: [apps/extract/README.md](apps/extract/README.md)

## Configurando o Ambiente

Requisitos atuais:

- Pyenv `3.x`
- Python `3.14.2`
- Poetry `2.x`
- PostgreSQL disponivel localmente ou em container

Defina a versao local do Python:

```bash
pyenv local 3.14.2
```

Instalacao das dependencias:

```bash
poetry install
```

A execucao dos modulos fica documentada em cada aplicativo.

## Modelo de Dados

O modelo ERD do projeto esta em:

```text
src/forlife_insurance/assets/database_diagrama.erd.json
```

Esse artefato representa a base relacional compartilhada pelos aplicativos do
repositorio.
