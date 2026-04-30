# Forlife Insurance Workspace

Workspace de estudos de engenharia de dados para o domínio de seguros da
Forlife. O código foi organizado em projetos independentes dentro de
`projects/`, cada um com pacote, dependências e entrypoints próprios.

## Projetos

| Projeto | Responsabilidade | Caminho |
| --- | --- | --- |
| Core | Biblioteca compartilhada com configuração, banco, ORM models e ERD. | `projects/forlife-insurance-core` |
| Seed | Geração e carga de dados sintéticos no PostgreSQL. | `projects/forlife-insurance-seed` |
| API | API transacional para consumo de aplicações. | `projects/forlife-insurance-api` |
| Extract | API e job de extração analítica incremental. | `projects/forlife-insurance-extract` |

O pedido funcional foi separar em `seed`, `api` e `extract`. O `core` fica como
biblioteca interna para evitar duplicação de modelos, conexão e configuração
entre os tres projetos.

## Estrutura

```text
projects/
  forlife-insurance-core/
    src/forlife_insurance_core/
  forlife-insurance-seed/
    src/forlife_insurance_seed/
  forlife-insurance-api/
    src/forlife_insurance_api/
  forlife-insurance-extract/
    src/forlife_insurance_extract/
```

## Dependencias Entre Projetos

```text
forlife-insurance-core
  <- forlife-insurance-seed
  <- forlife-insurance-api
  <- forlife-insurance-extract
```

Boas praticas aplicadas nesta divisao:

- O `core` concentra somente código compartilhado de domínio e infraestrutura.
- `seed`, `api` e `extract` dependem do `core`, não entre si.
- Cada projeto possui `pyproject.toml` próprio.
- Os contratos da API e da extração ficam nos projetos consumidores.
- Os entrypoints CLI ficam declarados apenas nos projetos que os executam.

## Preparacao

Crie um `.env` em cada projeto que for executar, usando o `.env.example` do
próprio projeto.

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
```

## Executar Seed

```bash
cd projects/forlife-insurance-seed
poetry install
poetry run forlife-seed --mode once --batch-size 20
```

## Executar API

```bash
cd projects/forlife-insurance-api
poetry install
poetry run uvicorn forlife_insurance_api.app:app --reload
```

## Executar Extract

```bash
cd projects/forlife-insurance-extract
poetry install
poetry run uvicorn forlife_insurance_extract.app:app --reload
poetry run forlife-extract-apolices --output-path ./out/apolices.ndjson
```

## Documentação

- [Arquitetura](docs/architecture.md)
- [Guia de desenvolvimento](docs/development.md)
- [Core](projects/forlife-insurance-core/README.md)
- [Seed](projects/forlife-insurance-seed/README.md)
- [API](projects/forlife-insurance-api/README.md)
- [Extract](projects/forlife-insurance-extract/README.md)
