# Containerização Forlife Insurance — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Criar `Dockerfile` e `docker-compose.yml` para subir PostgreSQL 18, rodar seed de 100 apólices e iniciar API e UI com um único `docker compose up`.

**Architecture:** Um único `Dockerfile` serve de base para os três serviços Python (seed, api, ui) — eles compartilham o mesmo virtualenv Poetry. O `docker-compose.yml` orquestra 4 containers com ordem de inicialização garantida via `depends_on` + `healthcheck`. Nenhuma alteração de código-fonte é necessária; `API_BASE_URL` já é configurável via env var em `api_client.py`.

**Tech Stack:** Docker, Docker Compose v2, python:3.12-slim, postgres:18, Poetry, uvicorn, Streamlit.

---

## Mapa de arquivos

| Arquivo | Ação | Responsabilidade |
|---|---|---|
| `Dockerfile` | Criar | Imagem Python única para api, ui e seed |
| `docker-compose.yml` | Criar | Orquestração dos 4 serviços com healthcheck e volumes |

---

## Task 1: Dockerfile

**Files:**
- Create: `Dockerfile`

- [ ] **Step 1: Escrever o Dockerfile**

Crie `Dockerfile` na raiz do repositório com o seguinte conteúdo:

```dockerfile
FROM python:3.12-slim

ENV POETRY_NO_INTERACTION=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
    && poetry install --without dev --no-root \
    && rm -rf $POETRY_CACHE_DIR

COPY projects/ ./projects/

RUN poetry install --without dev
```

**Por que dois passos de `poetry install`?**
O primeiro (`--no-root`) instala só as dependências externas (sqlalchemy, fastapi, etc.) sem copiar o código-fonte ainda — essa layer fica em cache enquanto `poetry.lock` não mudar. O segundo instala os pacotes do monorepo após o código estar disponível.

- [ ] **Step 2: Verificar o build**

```bash
docker build -t forlife:test .
```

Expected: build finaliza com `Successfully built <id>` (pode levar 2-3 min na primeira vez — downloads das deps).

- [ ] **Step 3: Verificar que os pacotes foram instalados corretamente**

```bash
docker run --rm forlife:test python -c "import forlife_insurance_api; import forlife_insurance_core; import forlife_insurance_seed; print('OK')"
```

Expected:
```
OK
```

- [ ] **Step 4: Commit**

```bash
git add Dockerfile
git commit -m "build: adiciona Dockerfile para imagem Python única dos serviços"
```

---

## Task 2: docker-compose.yml

**Files:**
- Create: `docker-compose.yml`

- [ ] **Step 1: Escrever o docker-compose.yml**

Crie `docker-compose.yml` na raiz do repositório:

```yaml
services:
  postgres:
    image: postgres:18
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER} -d ${DB_NAME}"]
      interval: 5s
      timeout: 5s
      retries: 10
    ports:
      - "${DB_PORT:-5432}:5432"

  seed:
    build: .
    command: python projects/forlife_insurance_seed/runner.py --mode once --batch-size 100
    env_file: .env
    environment:
      DB_HOST: postgres
    depends_on:
      postgres:
        condition: service_healthy
    restart: "no"

  api:
    build: .
    command: uvicorn forlife_insurance_api.app:app --host 0.0.0.0 --port 8000
    env_file: .env
    environment:
      DB_HOST: postgres
    depends_on:
      postgres:
        condition: service_healthy
    ports:
      - "8000:8000"
    restart: unless-stopped

  ui:
    build: .
    command: streamlit run projects/forlife_insurance_ui/app.py --server.address 0.0.0.0
    env_file: .env
    environment:
      API_BASE_URL: http://api:8000
    depends_on:
      - api
    ports:
      - "8501:8501"
    restart: unless-stopped

volumes:
  postgres_data:
```

**Notas de design:**
- `seed` e `api` sobem em paralelo após postgres ficar saudável — a API inicia sem dados e o seed os insere; não há conflito
- `ui` usa `service_started` (padrão do `depends_on` com lista) para `api` — o Streamlit exibe erros temporários até a API estar pronta, que é comportamento aceitável
- `DB_HOST: postgres` sobrescreve o `DB_HOST=localhost` do `.env` local para os serviços que falam com o banco
- `API_BASE_URL: http://api:8000` sobrescreve `http://localhost:8000` do `.env` local para a UI

- [ ] **Step 2: Garantir que o .env existe com as credenciais**

Se não existir, copie o exemplo:
```bash
cp .env-example .env
```

Edite `.env` e preencha `DB_USER`, `DB_PASSWORD` e `DB_NAME`. Exemplo:
```
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=seguros
API_BASE_URL=http://localhost:8000
```

> O `DB_HOST` e `API_BASE_URL` no `.env` são usados apenas para desenvolvimento local. Para Docker, o `docker-compose.yml` os sobrescreve via `environment:`.

- [ ] **Step 3: Validar sintaxe do compose**

```bash
docker compose config
```

Expected: imprime o YAML expandido sem erros.

- [ ] **Step 4: Commit**

```bash
git add docker-compose.yml
git commit -m "build: adiciona docker-compose.yml com postgres, seed, api e ui"
```

---

## Task 3: Verificação end-to-end

**Files:** nenhum arquivo novo — apenas verificação.

- [ ] **Step 1: Subir o stack completo**

```bash
docker compose up --build
```

Acompanhe os logs. Sequência esperada:
1. `postgres` sobe e passa o healthcheck (~10s)
2. `seed` e `api` sobem em paralelo
3. `seed` imprime algo como `Batch concluido: corretores=X, clientes=Y, apólices=100, ...` e encerra
4. `api` fica em execução com `Application startup complete.`
5. `ui` sobe e exibe `You can now view your Streamlit app in your browser`

- [ ] **Step 2: Verificar a API**

```bash
curl http://localhost:8000/apolices?limit=5
```

Expected: JSON com lista de apólices (não vazia após o seed terminar).

- [ ] **Step 3: Verificar a UI**

Abra `http://localhost:8501` no navegador. A dashboard deve carregar e exibir dados.

- [ ] **Step 4: Verificar persistência de dados**

```bash
docker compose down
docker compose up -d
```

Aguarde os serviços subirem e repita o Step 2. Os dados devem persistir (volume `postgres_data` preservado). O `seed` não roda novamente porque `restart: "no"` não reinicia containers encerrados com sucesso — para re-seeder, use `docker compose run seed`.

- [ ] **Step 5: Commit final**

```bash
git add .
git commit -m "build: containerização completa da plataforma Forlife Insurance"
```
