# Design: Migração para Monorepo Flat com Venv Único

**Data:** 2026-05-08
**Status:** Aprovado

## Contexto

O repositório `forlife-insurance-company` é um monorepo com quatro sub-projetos em `projects/`. Atualmente cada sub-projeto tem seu próprio `pyproject.toml`, `poetry.lock` e `.venv`. Essa estrutura gera fricção desnecessária para um projeto de portfólio com um único desenvolvedor: múltiplos ambientes virtuais para manter, comandos prefixados com `cd project && poetry run`, e uma tarefa `install` que instala quatro projetos sequencialmente.

## Objetivo

Consolidar tudo em um único ambiente virtual e eliminar os `pyproject.toml` individuais, mantendo os pacotes organizados dentro de `projects/` como módulos Python diretamente acessíveis.

## Estrutura Final

```
forlife-insurance-company/
├── pyproject.toml                    ← único, consolida todas as dependências
├── poetry.lock                       ← único lock file
├── README.md                         ← único README
├── .env / .env.example
├── .python-version
├── .gitignore
└── projects/
    ├── forlife_insurance_core/       ← era forlife-insurance-core/src/forlife_insurance_core/
    │   ├── __init__.py
    │   ├── config.py
    │   ├── database/
    │   └── models/
    ├── forlife_insurance_api/        ← era forlife-insurance-api/src/forlife_insurance_api/
    │   ├── __init__.py
    │   ├── app.py
    │   ├── routers/
    │   ├── schemas/
    │   └── services/
    ├── forlife_insurance_seed/       ← era forlife-insurance-seed/src/forlife_insurance_seed/
    │   ├── __init__.py
    │   └── ...
    └── forlife_insurance_ui/         ← era forlife-insurance-ui/
        ├── app.py
        ├── pages/
        └── services/
```

## Mudanças no `pyproject.toml` raiz

### `package-mode`

Remover `package-mode = false`. Com `package-mode = true` (padrão) é possível declarar os pacotes a instalar e os scripts CLI.

### `packages`

```toml
packages = [
    { include = "forlife_insurance_core", from = "projects" },
    { include = "forlife_insurance_api",  from = "projects" },
    { include = "forlife_insurance_seed", from = "projects" },
]
```

`forlife_insurance_ui` não é declarado como pacote porque é um app Streamlit, não uma biblioteca. O Streamlit adiciona `projects/forlife_insurance_ui/` ao `sys.path` automaticamente ao rodar `app.py`.

### Dependências consolidadas

Todas as dependências das quatro sub-projetos entram em `[tool.poetry.dependencies]`:

| Dependência | Origem |
|---|---|
| `sqlalchemy` | core |
| `python-dotenv` | core + ui |
| `psycopg2-binary` | core |
| `fastapi` | api |
| `uvicorn` | api |
| `pydantic` | api |
| `pydantic-extra-types[phonenumbers]` | api |
| `pydantic-br` | api |
| `email-validator` | api |
| `faker` | seed |
| `streamlit` | ui |
| `httpx` | ui |
| `pandas` | ui |

### Scripts

```toml
[tool.poetry.scripts]
forlife-seed = "forlife_insurance_seed.runner:main"
```

### Tasks Taskipy (simplificadas)

```toml
[tool.taskipy.tasks]
lint       = { cmd = "black projects && isort projects",                        help = "Formata código" }
lint-check = { cmd = "black --check projects && isort --check projects",        help = "Verifica formatação (CI)" }
security   = { cmd = "bandit -r projects -lll",                                 help = "Scan de segurança" }
test       = { cmd = "pytest",                                                  help = "Roda testes" }
api        = { cmd = "uvicorn forlife_insurance_api.app:app --reload",          help = "Sobe a API" }
ui         = { cmd = "streamlit run projects/forlife_insurance_ui/app.py",      help = "Sobe o Streamlit" }
seed       = { cmd = "forlife-seed --mode once --batch-size 20",               help = "Seed do banco" }
```

## Análise de Imports — Nenhuma Alteração de Código Necessária

| Projeto | Import | Situação |
|---|---|---|
| API → Core | `from forlife_insurance_core.xxx import yyy` | Sem mudança — nome do pacote não muda |
| API interna | `from forlife_insurance_api.routers.xxx import ...` | Sem mudança |
| Seed → Core | `from forlife_insurance_core.models.xxx import ...` | Sem mudança |
| Seed interna | `from forlife_insurance_seed.xxx import ...` | Sem mudança |
| UI → services | `from services.api_client import ApiClient` | Sem mudança — Streamlit gerencia o `sys.path` |

Os nomes dos pacotes Python (`forlife_insurance_core`, `forlife_insurance_api`, `forlife_insurance_seed`) não mudam — apenas o local no disco. O Poetry registra os pacotes no venv via a declaração `packages`, então todos os imports existentes continuam funcionando sem nenhuma alteração.

## Sequência de Migração

**Passo 1 — Mover os pacotes (sem alterar código):**
- `projects/forlife-insurance-core/src/forlife_insurance_core/` → `projects/forlife_insurance_core/`
- `projects/forlife-insurance-api/src/forlife_insurance_api/` → `projects/forlife_insurance_api/`
- `projects/forlife-insurance-seed/src/forlife_insurance_seed/` → `projects/forlife_insurance_seed/`
- `projects/forlife-insurance-ui/{app.py,pages/,services/,.streamlit/}` → `projects/forlife_insurance_ui/`

**Passo 2 — Atualizar o `pyproject.toml` raiz:**
- Remover `package-mode = false`
- Adicionar bloco `packages`
- Consolidar todas as dependências
- Migrar scripts e tasks

**Passo 3 — Limpar o que sobrou:**
- Deletar pastas `projects/forlife-insurance-{core,api,seed,ui}/` (com hífen — agora vazias)
- Deletar `.venv` dos sub-projetos
- Deletar `README.md` dos sub-projetos
- Deletar `pyproject.toml` e `poetry.lock` dos sub-projetos

**Passo 4 — Instalar e verificar:**
```bash
poetry install
poetry run task lint-check
poetry run task test
```

## O Que Não Muda

- Nomes dos pacotes Python — todos os imports continuam válidos
- Lógica de negócio — nenhum arquivo de código é alterado
- Hierarquia de dependência: Core ← API, Seed (o Core continua sendo a base)
- Variáveis de ambiente — o `.env` na raiz já é compartilhado
- Configuração do `.streamlit/config.toml` — migra junto com a UI
