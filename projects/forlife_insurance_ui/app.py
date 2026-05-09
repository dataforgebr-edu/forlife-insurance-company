import streamlit as st

st.set_page_config(
    page_title="ForLife Insurance",
    page_icon="🛡️",
    layout="wide",
)

st.title("ForLife Insurance — Plataforma de Gestão")
st.markdown(
    """
Bem-vindo à interface de gestão do portfólio ForLife Insurance.

Use o menu lateral para navegar entre as entidades do sistema.

---

### Arquitetura do sistema

```
Faker/Seed  →  PostgreSQL  →  FastAPI  →  Streamlit (você está aqui)
```

| Módulo | Descrição |
|---|---|
| **Apólices** | Contratos de seguro de vida emitidos |
| **Clientes** | Segurados vinculados às apólices |
| **Corretores** | Empresas intermediárias de venda |
| **Sinistros** | Ocorrências de acionamento do seguro |
| **Parcelas** | Pagamentos periódicos das apólices |

---

> Registros não são excluídos — apenas inativados via mudança de status,
> conforme a regra de negócio de seguros.
"""
)
