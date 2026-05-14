# Design: Containerização Forlife Insurance

**Data:** 2026-05-14  
**Status:** Aprovado

## Objetivo

Containerizar a plataforma Forlife Insurance para que, com um único comando (`docker compose up`), seja possível subir o PostgreSQL, rodar o seed de 100 apólices, iniciar a API e iniciar a UI.

## Arquivos a criar

- `Dockerfile` — imagem Python única para API, UI e seed
- `docker-compose.yml` — orquestração dos 4 serviços

## Dockerfile

**Base:** `python:3.12-slim`

**Estratégia de instalação de dependências:**
- Instala Poetry via `pip install poetry`
- Configura `virtualenvs.create = false` para instalar pacotes direto no Python do sistema (mais simples em containers)
- Copia `pyproject.toml` e `poetry.lock` antes do código-fonte para aproveitar o cache de layers do Docker
- Instala dependências de produção (`--without dev`)
- Copia o código-fonte completo (`projects/`)
- Instala os pacotes do monorepo (`poetry install --without dev`)
- Sem `CMD` — cada serviço define seu próprio comando no docker-compose

## docker-compose.yml

### Serviços

| Serviço  | Imagem         | Porta  | Comando                                                                                       | Depende de              |
|----------|----------------|--------|-----------------------------------------------------------------------------------------------|-------------------------|
| postgres | postgres:18    | 5432   | padrão                                                                                        | —                       |
| seed     | build local    | —      | `python projects/forlife_insurance_seed/runner.py --mode once --batch-size 100`               | postgres saudável       |
| api      | build local    | 8000   | `uvicorn forlife_insurance_api.app:app --host 0.0.0.0 --port 8000`                           | postgres saudável       |
| ui       | build local    | 8501   | `streamlit run projects/forlife_insurance_ui/app.py --server.address 0.0.0.0`                | api iniciada            |

### Detalhes de orquestração

- **postgres** tem `healthcheck` com `pg_isready -U $POSTGRES_USER` — seed e API só sobem após o banco estar aceitando conexões (`condition: service_healthy`)
- **seed** tem `restart: "no"` — job one-shot, encerra após completar o batch de 100 apólices
- **api e ui** têm `restart: unless-stopped`
- Volume nomeado `postgres_data` para persistência dos dados

### Estratégia de variáveis de ambiente

O usuário mantém um único `.env` (copiado do `.env-example`) com as credenciais. O docker-compose usa `env_file: .env` em todos os serviços Python e sobrescreve via `environment:` apenas os valores que mudam no contexto Docker:

| Var             | Valor local       | Valor Docker       | Serviço(s) afetado(s) |
|-----------------|-------------------|--------------------|-----------------------|
| `DB_HOST`       | `localhost`       | `postgres`         | seed, api             |
| `API_BASE_URL`  | `http://localhost:8000` | `http://api:8000` | ui                |

O serviço `postgres` recebe `POSTGRES_USER`, `POSTGRES_PASSWORD` e `POSTGRES_DB` mapeados diretamente do `.env`.

## Sem mudanças de código

O `api_client.py` já lê `API_BASE_URL` de variável de ambiente — nenhuma alteração no código-fonte é necessária.

## Porta de acesso

Após `docker compose up`:
- API: `http://localhost:8000`
- UI: `http://localhost:8501`
