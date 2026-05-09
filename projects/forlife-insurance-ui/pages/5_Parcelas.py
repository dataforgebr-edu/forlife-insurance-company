import pandas as pd
import streamlit as st
from services.api_client import ApiClient

st.set_page_config(page_title="Parcelas", layout="wide")
st.title("Parcelas")
st.caption("Pagamentos periódicos vinculados às apólices.")

api = ApiClient()


def _load_data(apolice_id: int | None = None):
    return api.get_parcelas(limit=500, apolice_id=apolice_id)


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
        "parcela_id",
        "apolice_id",
        "valor",
        "data_emissao",
        "data_periodo",
        "data_pagamento",
        "data_insercao",
        "data_atualizacao",
    ]
    st.dataframe(
        df[[c for c in display_cols if c in df.columns]], use_container_width=True
    )
else:
    st.info("Nenhuma parcela encontrada.")

# --- Criar ---
with st.expander("Criar nova parcela"):
    meios = api.get_meios_pagamento()
    meio_map = _dom_map(meios, "meio_pagamento_id")

    with st.form("form_create_parcela"):
        col1, col2 = st.columns(2)
        with col1:
            apolice_keys = [a["apolice_id"] for a in apolices]
            apolice_id = st.selectbox("Apólice", options=apolice_keys)
            valor = st.number_input("Valor (R$)", min_value=0.0, step=50.0)
            meio_pagamento_id = st.selectbox(
                "Meio de Pagamento",
                options=list(meio_map.keys()),
                format_func=lambda x: meio_map[x],
            )
        with col2:
            data_emissao = st.date_input("Data de Emissão")
            data_periodo = st.date_input("Data do Período")
            data_pagamento = st.date_input("Data de Pagamento")

        submitted = st.form_submit_button("Criar")
        if submitted:
            payload = {
                "apolice_id": apolice_id,
                "valor": valor,
                "meio_pagamento_id": meio_pagamento_id,
                "data_emissao": data_emissao.isoformat() + "T00:00:00",
                "data_periodo": data_periodo.isoformat() + "T00:00:00",
                "data_pagamento": data_pagamento.isoformat() + "T00:00:00",
            }
            result = api.create_parcela(payload)
            if "parcela_id" in result:
                st.success(f"Parcela #{result['parcela_id']} criada com sucesso.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")

# --- Editar ---
st.subheader("Editar parcela")
if data:
    ids = [r["parcela_id"] for r in data]
    selected_id = st.selectbox("Selecione a parcela", ids, key="edit_parcela_sel")
    record = next(r for r in data if r["parcela_id"] == selected_id)

    meios = api.get_meios_pagamento()
    meio_map = _dom_map(meios, "meio_pagamento_id")
    meio_keys = list(meio_map.keys())

    with st.form("form_edit_parcela"):
        col1, col2 = st.columns(2)
        with col1:
            new_valor = st.number_input(
                "Valor (R$)", value=float(record.get("valor", 0)), step=50.0
            )
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
        with col2:
            st.write(f"Emissão: `{record.get('data_emissao', '')}`")
            st.write(f"Período: `{record.get('data_periodo', '')}`")
            st.write(f"Pagamento: `{record.get('data_pagamento', '')}`")

        save = st.form_submit_button("Salvar alterações")
        if save:
            result = api.update_parcela(
                selected_id,
                {
                    "valor": new_valor,
                    "meio_pagamento_id": new_meio,
                },
            )
            if "parcela_id" in result:
                st.success("Parcela atualizada.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")
