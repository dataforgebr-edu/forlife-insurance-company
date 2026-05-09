# Design: Três Mudanças no Monorepo ForLife Insurance

**Data:** 2026-05-08
**Status:** Aprovado

---

## Visão Geral

Este documento descreve três mudanças independentes no monorepo `forlife-insurance-company`:

1. Remoção do sub-projeto `forlife-insurance-extract`
2. Remoção dos endpoints DELETE da API transacional
3. Criação do sub-projeto `forlife-insurance-ui` (Streamlit)

---

## Mudança 1 — Remoção do `forlife-insurance-extract`

### Motivação

O projeto de extração analítica não fará mais parte do portfólio. Sua remoção reduz o escopo do monorepo e elimina manutenção desnecessária.

### O que muda

- A pasta `projects/forlife-insurance-extract/` é removida por completo.
- O `pyproject.toml` raiz tem as referências ao extract removidas das tasks `install`, `lint`, `lint-check`, `security` e `test`.
- O `docs/architecture.md` é atualizado para remover o extract do diagrama e das fronteiras descritas.

### O que não muda

Os projetos `core`, `api` e `seed` não são afetados. O extract não tem dependentes diretos — ele apenas consumia o `core`.

---

## Mudança 2 — Remoção dos endpoints DELETE da API

### Motivação

Em um modelo de negócio de seguros, registros não são apagados — são inativados via mudança de status. Os endpoints DELETE nunca deveriam existir e estão sendo removidos para alinhar o código à regra de negócio.

### Escopo

5 routers possuem DELETE hoje: `apolice`, `cliente`, `corretor`, `parcela` e `sinistro`.

### O que muda

- Remove o handler `@router.delete(...)` de cada um dos 5 routers.
- Remove os métodos de delete dos services correspondentes, eliminando código morto.
- Nenhuma outra rota (GET, POST, PUT) é tocada.

---

## Mudança 3 — Novo projeto `forlife-insurance-ui` (Streamlit)

### Motivação

Criar uma interface visual para o portfólio que demonstre o sistema de ponta a ponta: seed → banco → API → UI. A interface deve ser simples, bonita e funcional, com CRUD completo (sem delete).

### Estrutura de arquivos

```
projects/forlife-insurance-ui/
├── pyproject.toml
├── .env.example              # API_BASE_URL=http://localhost:8000
├── .streamlit/
│   └── config.toml           # tema light clean
├── app.py                    # página Home (visão geral do sistema)
├── pages/
│   ├── 1_Apolices.py
│   ├── 2_Clientes.py
│   ├── 3_Corretores.py
│   ├── 4_Sinistros.py
│   └── 5_Parcelas.py
└── services/
    └── api_client.py         # wrapper HTTP para a FastAPI
```

### Tema

Arquivo `.streamlit/config.toml` com tema light clean:

```toml
[theme]
primaryColor = "#2563EB"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F8FAFC"
textColor = "#1E293B"
font = "sans serif"
```

### Padrão de cada página

1. Título e descrição da entidade
2. Tabela com todos os registros (`st.dataframe`)
3. Expansor "Criar novo" com formulário de criação (POST)
4. Seleção de registro para exibir formulário de edição (PUT)

### `services/api_client.py`

- Classe `ApiClient` com métodos nomeados por entidade: `get_apolices()`, `create_apolice()`, `update_apolice()`, etc.
- URL base lida da variável de ambiente `API_BASE_URL` via `python-dotenv`
- Usa `httpx` (síncrono) — sem necessidade de async no Streamlit

### Dependências

```toml
[tool.poetry.dependencies]
python = ">=3.12,<4.0"
streamlit = ">=1.35.0"
httpx = ">=0.27.0"
pandas = ">=2.2.0"
python-dotenv = ">=1.0.0"
```

### Integração no monorepo

As tasks do `pyproject.toml` raiz são atualizadas para incluir o `forlife-insurance-ui`:

- `install`: adiciona `poetry install --directory projects/forlife-insurance-ui`
- `lint` e `lint-check`: adiciona `black` e `isort` nas pastas `app.py`, `pages/` e `services/`
- `security`: adiciona `bandit` no projeto UI

Entrypoint para execução local:

```bash
cd projects/forlife-insurance-ui
poetry run streamlit run app.py
```

---

## Ordem de Implementação Recomendada

1. Remover o extract (sem risco, sem dependentes)
2. Remover os DELETEs da API (cirurgia simples nos routers/services)
3. Criar o projeto UI (maior esforço, depende da API estar estável)
