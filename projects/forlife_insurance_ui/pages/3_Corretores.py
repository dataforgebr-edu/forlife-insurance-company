import pandas as pd
import streamlit as st
from services.api_client import ApiClient

st.set_page_config(page_title="Corretores", layout="wide")
st.title("Corretores")
st.caption("Empresas intermediárias de venda de apólices.")

api = ApiClient()


def _load_data():
    return api.get_corretores(limit=500)


# --- Tabela ---
st.subheader("Registros")
data = _load_data()
if data:
    df = pd.DataFrame(data)
    display_cols = [
        "corretor_id",
        "nome",
        "cnpj",
        "email",
        "data_insercao",
        "data_atualizacao",
    ]
    st.dataframe(
        df[[c for c in display_cols if c in df.columns]], use_container_width=True
    )
else:
    st.info("Nenhum corretor encontrado.")

# --- Criar ---
with st.expander("Criar novo corretor"):
    estados = api.get_estados()
    estado_map = {e["estado_id"]: f"{e['uf']} — {e['descricao']}" for e in estados}

    with st.form("form_create_corretor"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome")
            cnpj = st.text_input("CNPJ (ex: 12.345.678/0001-90)")
        with col2:
            email = st.text_input("E-mail")
            estado_id = st.selectbox(
                "Estado",
                options=list(estado_map.keys()),
                format_func=lambda x: estado_map[x],
            )

        submitted = st.form_submit_button("Criar")
        if submitted:
            payload = {
                "nome": nome,
                "cnpj": cnpj,
                "email": email,
                "estado_id": estado_id,
            }
            result = api.create_corretor(payload)
            if "corretor_id" in result:
                st.success(f"Corretor #{result['corretor_id']} criado com sucesso.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")

# --- Editar ---
st.subheader("Editar corretor")
if data:
    ids = [r["corretor_id"] for r in data]
    selected_id = st.selectbox(
        "Selecione o corretor",
        ids,
        format_func=lambda x: next(r["nome"] for r in data if r["corretor_id"] == x),
        key="edit_corretor_sel",
    )
    record = next(r for r in data if r["corretor_id"] == selected_id)

    estados = api.get_estados()
    estado_map = {e["estado_id"]: f"{e['uf']} — {e['descricao']}" for e in estados}
    estado_keys = list(estado_map.keys())

    with st.form("form_edit_corretor"):
        col1, col2 = st.columns(2)
        with col1:
            new_nome = st.text_input("Nome", value=record.get("nome", ""))
            new_cnpj = st.text_input("CNPJ", value=record.get("cnpj", ""))
        with col2:
            new_email = st.text_input("E-mail", value=record.get("email", ""))
            cur_estado = (
                record["estado"]["estado_id"]
                if isinstance(record.get("estado"), dict)
                else estado_keys[0]
            )
            new_estado = st.selectbox(
                "Estado",
                options=estado_keys,
                index=estado_keys.index(cur_estado) if cur_estado in estado_keys else 0,
                format_func=lambda x: estado_map[x],
            )

        save = st.form_submit_button("Salvar alterações")
        if save:
            result = api.update_corretor(
                selected_id,
                {
                    "nome": new_nome,
                    "cnpj": new_cnpj,
                    "email": new_email,
                    "estado_id": new_estado,
                },
            )
            if "corretor_id" in result:
                st.success("Corretor atualizado.")
                st.rerun()
            else:
                st.error(f"Erro: {result}")
