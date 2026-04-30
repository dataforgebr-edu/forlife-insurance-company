# API App

Aplicativo responsavel pela API transacional do dominio de seguros.

Este README cobre a interface HTTP principal do projeto. Para a visao geral do
repositorio, consulte [README.md](../../README.md).

## Objetivo

Expor os dados do dominio com foco em consumo transacional e integracoes de
produto.

O foco aqui e:

- leitura de apolices e entidades relacionadas;
- contratos mais ricos e navegaveis para a camada de aplicacao;
- reutilizacao dos models ORM compartilhados pelo pacote principal;
- separacao clara em relacao a camada `extract`.

## Codigo Relacionado

A implementacao da API esta em `src/forlife_insurance/api`.

Principais modulos:

- `routers/`: rotas HTTP da API.
- `schemas/`: modelos Pydantic para resposta e serializacao.
- `services/`: regras de consulta e orquestracao da camada de aplicacao.

## Estrutura atual

Hoje a API esta focada em leitura de apolices e entidades de apoio. O desenho
segue a mesma base relacional utilizada pelo seed e pelo extract, mas com
contratos mais completos para consumo de aplicacao.

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

Preencha as variaveis de banco:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Observacoes de Arquitetura

- A API transacional e separada da camada `extract`.
- Os schemas de resposta usam nomes alinhados ao dominio.
- O pacote `src/forlife_insurance/models` e a fonte principal do modelo
  relacional compartilhado.
- A pasta `api` hoje concentra contratos, servicos e routers; o entrypoint
  FastAPI dedicado pode ser adicionado quando a interface precisar ser
  publicada separadamente.
