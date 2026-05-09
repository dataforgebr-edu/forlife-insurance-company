import pandas as pd
import streamlit as st
from services.api_client import ApiClient

st.set_page_config(page_title="Apólices", layout="wide")
st.title("Apólices")
st.caption("Contratos de seguro de vida emitidos pela plataforma.")

api = ApiClient()


def _load_data():
    return api.get_apolices(limit=500)


def _dom_map(items: list[dict], id_key: str, label_key: str = "descricao") -> dict:
    return {item[id_key]: item[label_key] for item in items}


# --- Tabela ---
st.subheader("Registros")
data = _load_data()
if data:
    df = pd.DataFrame(data)
    display_cols = [
        "apolice_id",
        "cliente_id",
        "corretor_id",
        "capital_segurado",
        "premio",
        "inicio_vigencia",
        "fim_vigencia",
        "data_insercao",
        "data_atualizacao",
    ]
    st.dataframe(
        df[[c for c in display_cols if c in df.columns]], use_container_width=True
    )
else:
    st.info("Nenhuma apólice encontrada.")

# --- Criar ---
with st.expander("Criar nova apólice"):
    produtos = api.get_produtos()
    status_opts = api.get_status_apolice()
    periodicidades = api.get_periodicidades()
    meios = api.get_meios_pagamento()
    clientes = api.get_clientes(limit=500)
    corretores = api.get_corretores(limit=500)

    prod_map = _dom_map(produtos, "produto_id")
    status_map = _dom_map(status_opts, "status_apolice_id")
    per_map = _dom_map(periodicidades, "periodicidade_id")
    meio_map = _dom_map(meios, "meio_pagamento_id")
    cli_map = {c["cliente_id"]: c["nome"] for c in clientes}
    cor_map = {c["corretor_id"]: c["nome"] for c in corretores}

    with st.form("form_create_apolice"):
        col1, col2 = st.columns(2)
        with col1:
            cliente_id = st.selectbox(
                "Cliente",
                options=list(cli_map.keys()),
                format_func=lambda x: cli_map[x],
            )
            corretor_id = st.selectbox(
                "Corretor",
                options=list(cor_map.keys()),
                format_func=lambda x: cor_map[x],
            )
            produto_id = st.selectbox(
                "Produto",
                options=list(prod_map.keys()),
                format_func=lambda x: prod_map[x],
            )
            status_apolice_id = st.selectbox(
                "Status",
                options=list(status_map.keys()),
                format_func=lambda x: status_map[x],
            )
        with col2:
            periodicidade_id = st.selectbox(
                "Periodicidade",
                options=list(per_map.keys()),
                format_func=lambda x: per_map[x],
            )
            meio_pagamento_id = st.selectbox(
                "Meio de Pagamento",
                options=list(meio_map.keys()),
                format_func=lambda x: meio_map[x],
            )
            capital_segurado = st.number_input(
                "Capital Segurado (R$)", min_value=0.0, step=1000.0
            )
            premio = st.number_input("Prêmio (R$)", min_value=0.0, step=100.0)
            inicio_vigencia = st.date_input("Início Vigência")
            fim_vigencia = st.date_input("Fim Vigência")

        submitted = st.form_submit_button("Criar")
        if submitted:
            payload = {
                "cliente_id": cliente_id,
                "corretor_id": corretor_id,
                "produto_id": produto_id,
                "status_apolice_id": status_apolice_id,
                "periodicidade_id": periodicidade_id,
                "meio_pagamento_id": meio_pagamento_id,
                "capital_segurado": capital_segurado,
                "premio": premio,
                "inicio_vigencia": inicio_vigencia.isoformat() + "T00:00:00",
                "fim_vigencia": fim_vigencia.isoformat() + "T00:00:00",
            }
            result = api.create_apolice(payload)
            if "apolice_id" in result:
                st.success(f"Apólice #{result['apolice_id']} criada com sucesso.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")

# --- Editar ---
st.subheader("Editar apólice")
if data:
    ids = [r["apolice_id"] for r in data]
    selected_id = st.selectbox("Selecione a apólice", ids, key="edit_apolice_sel")
    record = next(r for r in data if r["apolice_id"] == selected_id)

    if not (
        "produto_id" in record
        and "status_apolice_id" in record
        and "periodicidade_id" in record
        and "meio_pagamento_id" in record
    ):
        detail = api.get_apolice(selected_id)
    else:
        detail = record

    produtos = api.get_produtos()
    status_opts = api.get_status_apolice()
    periodicidades = api.get_periodicidades()
    meios = api.get_meios_pagamento()
    prod_map = _dom_map(produtos, "produto_id")
    status_map = _dom_map(status_opts, "status_apolice_id")
    per_map = _dom_map(periodicidades, "periodicidade_id")
    meio_map = _dom_map(meios, "meio_pagamento_id")

    with st.form("form_edit_apolice"):
        col1, col2 = st.columns(2)
        with col1:
            new_capital = st.number_input(
                "Capital Segurado (R$)",
                value=float(detail.get("capital_segurado", 0)),
                step=1000.0,
            )
            new_premio = st.number_input(
                "Prêmio (R$)", value=float(detail.get("premio", 0)), step=100.0
            )
        with col2:
            prod_keys = list(prod_map.keys())
            cur_prod = (
                detail["produto"]["produto_id"]
                if isinstance(detail.get("produto"), dict)
                else detail.get("produto_id", prod_keys[0])
            )
            new_produto = st.selectbox(
                "Produto",
                options=prod_keys,
                index=prod_keys.index(cur_prod) if cur_prod in prod_keys else 0,
                format_func=lambda x: prod_map[x],
            )
            status_keys = list(status_map.keys())
            cur_status = (
                detail["status_apolice"]["status_apolice_id"]
                if isinstance(detail.get("status_apolice"), dict)
                else detail.get("status_apolice_id", status_keys[0])
            )
            new_status = st.selectbox(
                "Status",
                options=status_keys,
                index=status_keys.index(cur_status) if cur_status in status_keys else 0,
                format_func=lambda x: status_map[x],
            )

        save = st.form_submit_button("Salvar alterações")
        if save:
            result = api.update_apolice(
                selected_id,
                {
                    "capital_segurado": new_capital,
                    "premio": new_premio,
                    "produto_id": new_produto,
                    "status_apolice_id": new_status,
                },
            )
            if "apolice_id" in result:
                st.success("Apólice atualizada.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")
