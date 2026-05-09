import pandas as pd
import streamlit as st
from services.api_client import ApiClient

st.set_page_config(page_title="Sinistros", layout="wide")
st.title("Sinistros")
st.caption("Ocorrências de acionamento do seguro registradas na plataforma.")

api = ApiClient()


def _load_data(apolice_id: int | None = None):
    return api.get_sinistros(limit=500, apolice_id=apolice_id)


def _dom_map(items: list[dict], id_key: str, label_key: str = "descricao") -> dict:
    return {item[id_key]: item[label_key] for item in items}


# --- Filtro por apólice ---
apolices = api.get_apolices(limit=500)
apolice_opts = {0: "Todos"} | {
    a["apolice_id"]: f"Apólice #{a['apolice_id']}" for a in apolices
}
filtro_apolice = st.selectbox(
    "Filtrar por apólice",
    options=list(apolice_opts.keys()),
    format_func=lambda x: apolice_opts[x],
)
filter_id = filtro_apolice if filtro_apolice != 0 else None

# --- Tabela ---
st.subheader("Registros")
data = _load_data(filter_id)
if data:
    df = pd.DataFrame(data)
    display_cols = [
        "sinistro_id",
        "apolice_id",
        "valor",
        "data_pagamento",
        "data_insercao",
        "data_atualizacao",
    ]
    st.dataframe(
        df[[c for c in display_cols if c in df.columns]], use_container_width=True
    )
else:
    st.info("Nenhum sinistro encontrado.")

# --- Criar ---
with st.expander("Criar novo sinistro"):
    status_opts = api.get_status_sinistro()
    meios = api.get_meios_pagamento()
    status_map = _dom_map(status_opts, "status_sinistro_id")
    meio_map = _dom_map(meios, "meio_pagamento_id")

    with st.form("form_create_sinistro"):
        col1, col2 = st.columns(2)
        with col1:
            apolice_keys = list(
                {a["apolice_id"]: a["apolice_id"] for a in apolices}.keys()
            )
            apolice_id = st.selectbox("Apólice", options=apolice_keys)
            valor = st.number_input("Valor (R$)", min_value=0.0, step=100.0)
        with col2:
            data_pagamento = st.date_input("Data de Pagamento")
            status_sinistro_id = st.selectbox(
                "Status",
                options=list(status_map.keys()),
                format_func=lambda x: status_map[x],
            )
            meio_pagamento_id = st.selectbox(
                "Meio de Pagamento",
                options=list(meio_map.keys()),
                format_func=lambda x: meio_map[x],
            )

        submitted = st.form_submit_button("Criar")
        if submitted:
            payload = {
                "apolice_id": apolice_id,
                "valor": valor,
                "data_pagamento": data_pagamento.isoformat() + "T00:00:00",
                "status_sinistro_id": status_sinistro_id,
                "meio_pagamento_id": meio_pagamento_id,
            }
            result = api.create_sinistro(payload)
            if "sinistro_id" in result:
                st.success(f"Sinistro #{result['sinistro_id']} criado com sucesso.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")

# --- Editar ---
st.subheader("Editar sinistro")
if data:
    ids = [r["sinistro_id"] for r in data]
    selected_id = st.selectbox("Selecione o sinistro", ids, key="edit_sinistro_sel")
    record = next(r for r in data if r["sinistro_id"] == selected_id)

    status_opts = api.get_status_sinistro()
    meios = api.get_meios_pagamento()
    status_map = _dom_map(status_opts, "status_sinistro_id")
    meio_map = _dom_map(meios, "meio_pagamento_id")

    with st.form("form_edit_sinistro"):
        col1, col2 = st.columns(2)
        with col1:
            new_valor = st.number_input(
                "Valor (R$)", value=float(record.get("valor", 0)), step=100.0
            )
        with col2:
            status_keys = list(status_map.keys())
            cur_status = (
                record["status_sinistro"]["status_sinistro_id"]
                if isinstance(record.get("status_sinistro"), dict)
                else record.get("status_sinistro_id", status_keys[0])
            )
            new_status = st.selectbox(
                "Status",
                options=status_keys,
                index=status_keys.index(cur_status) if cur_status in status_keys else 0,
                format_func=lambda x: status_map[x],
            )
            meio_keys = list(meio_map.keys())
            cur_meio = (
                record["meio_pagamento"]["meio_pagamento_id"]
                if isinstance(record.get("meio_pagamento"), dict)
                else record.get("meio_pagamento_id", meio_keys[0])
            )
            new_meio = st.selectbox(
                "Meio de Pagamento",
                options=meio_keys,
                index=meio_keys.index(cur_meio) if cur_meio in meio_keys else 0,
                format_func=lambda x: meio_map[x],
            )

        save = st.form_submit_button("Salvar alterações")
        if save:
            result = api.update_sinistro(
                selected_id,
                {
                    "valor": new_valor,
                    "status_sinistro_id": new_status,
                    "meio_pagamento_id": new_meio,
                },
            )
            if "sinistro_id" in result:
                st.success("Sinistro atualizado.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")
