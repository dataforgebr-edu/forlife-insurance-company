# Arquitetura

## Visão Geral

O repositório foi separado em projetos independentes para reduzir acoplamento e
preparar a evolução para pipelines, orquestração e camadas analíticas.

```text
PostgreSQL
  ^
  |
forlife-insurance-core
  |-- database/session
  |-- models ORM
  |-- configuração
  |-- assets ERD
  |
  |-- forlife-insurance-seed
  |-- forlife-insurance-api
  `-- forlife-insurance-extract
```

## Fronteiras

### Core

Biblioteca interna compartilhada. Deve conter apenas recursos que todos os
projetos podem reutilizar sem criar dependencia circular.

Responsabilidades:

- leitura de variáveis de ambiente;
- criação de engine e sessões SQLAlchemy;
- base declarativa;
- modelos ORM;
- assets compartilhados, como o ERD.

Nao deve conter:

- rotas HTTP;
- jobs especificos;
- schemas Pydantic de API ou extract;
- lógica de geração de dados fake.

### Seed

Projeto responsável por criar massa sintética coerente para o banco
transacional.

Responsabilidades:

- carregar tabelas de domínio;
- gerar clientes, corretores, apólices, parcelas e sinistros;
- executar em modo pontual ou continuo;
- usar `forlife-insurance-core` como fonte de models e banco.

### API

Projeto responsável por expor dados para consumo transacional de aplicações.

Responsabilidades:

- rotas FastAPI;
- schemas Pydantic ricos e navegáveis;
- services de consulta voltados a produto;
- tratamento de erros HTTP.

### Extract

Projeto responsável por expor dados para consumo analítico e pipelines.

Responsabilidades:

- rotas FastAPI de extração;
- schemas planos e estáveis;
- consultas incrementais por watermark e chave;
- job CLI para exportacao NDJSON.

## Regras de Dependencia

- `core` não importa `seed`, `api` nem `extract`.
- `seed`, `api` e `extract` podem importar `core`.
- `api` não importa `extract`.
- `extract` não importa `api`.
- `seed` não importa `api` nem `extract`.
- Projetos novos devem ser criados dentro de `projects/`.

## Evolucao Recomendada

1. Criar testes por projeto.
2. Adicionar CI para lint, type check e testes.
3. Criar contratos de dados para o `extract`.
4. Integrar o `extract` a um orquestrador como Airflow.
5. Evoluir a saída analítica para camadas raw, silver e gold.
