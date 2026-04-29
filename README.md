# Forlife Insurance Company

Projeto de dados para uma seguradora que vende apólices nos segmentos de vida,
automóvel e residência.

O repositório concentra a base transacional do domínio e os aplicativos que
operam sobre ela. Hoje o foco está em dois fluxos principais:

- geração de dados sintéticos coerentes com as regras de negócio da seguradora;
- exposição desses dados por meio de uma API.

## Visão Geral

O projeto foi organizado como um monorepo simples com um pacote Python
compartilhado e documentação separada por aplicativo.

- `seed`: cria e popula a base PostgreSQL com dados sintéticos.
- `api`: expõe os dados do projeto para consumo por aplicações, estudos e
  integrações.

Os dois apps compartilham os mesmos módulos de domínio, conexão com banco e
modelos relacionais, evitando duplicação de regras e mantendo uma única fonte
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

  src/
    forlife_insurance/
      core/
      database/
      models/
      seed/
      assets/
```

## Package Python

O código compartilhado fica em `src/forlife_insurance`.

- `core/`: configuração da aplicação e leitura de variáveis de ambiente.
- `database/`: engine, sessões e base do SQLAlchemy.
- `models/`: definição das tabelas e relacionamentos.
- `seed/`: implementação do processo de carga sintética.
- `assets/`: artefatos de apoio, incluindo o diagrama ERD.

## Aplicativos

### Seed

Responsável por criar a estrutura relacional e popular o banco com dados
sintéticos consistentes com o domínio de seguros.

Documentação: [apps/seed/README.md](apps/seed/README.md)

### API

Responsável por expor os dados do projeto por HTTP, reaproveitando os modelos e
módulos compartilhados do pacote principal.

Documentação: [apps/api/README.md](apps/api/README.md)

## Configurando o Ambiente

Requisitos atuais:

- Pyenv `3.x`
- Python `3.14.2`
- Poetry `2.x`
- PostgreSQL disponível localmente ou em container

Defina a versão local do Python:

```bash
pyenv local 3.14.2
```

Instalação das dependências:

```bash
poetry install
```

A execução dos módulos fica documentada em cada aplicativo.

## Modelo de Dados

O modelo ERD do projeto está em:

```text
src/forlife_insurance/assets/database_diagrama.erd.json
```

Esse artefato representa a base relacional compartilhada pelos aplicativos do
repositório.
