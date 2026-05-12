import pandas as pd
import streamlit as st
from services.api_client import ApiClient

st.set_page_config(page_title="Clientes", layout="wide")
st.title("Clientes")
st.caption("Segurados vinculados às apólices da plataforma.")

api = ApiClient()


def _load_data():
    return api.get_clientes(limit=500)


@st.cache_data(ttl=300)
def _get_estados():
    return api.get_estados()


@st.cache_data(ttl=300)
def _get_cidades(estado_id):
    return api.get_cidades(estado_id)


# --- Tabela ---
st.subheader("Registros")
data = _load_data()
if data:
    df = pd.DataFrame(data)
    display_cols = [
        "cliente_id",
        "nome",
        "email",
        "telefone",
        "endereco",
        "data_nascimento",
        "data_insercao",
        "data_atualizacao",
    ]
    st.dataframe(
        df[[c for c in display_cols if c in df.columns]], use_container_width=True
    )
else:
    st.info("Nenhum cliente encontrado.")


# --- Criar ---
# @st.fragment isola o rerun: ao mudar estado só este bloco recarrega,
# sem st.form os widgets disparam rerun imediatamente, permitindo o cascade.
@st.fragment
def _criar_cliente():
    estados = _get_estados()
    estado_map = {e["estado_id"]: f"{e['uf']} — {e['descricao']}" for e in estados}

    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("Nome", key="c_nome")
        email = st.text_input("E-mail", key="c_email")
        telefone = st.text_input("Telefone (ex: +55 11 91234-5678)", key="c_telefone")
    with col2:
        endereco = st.text_input("Endereço", key="c_endereco")
        data_nascimento = st.date_input("Data de Nascimento", key="c_data_nasc")
        estado_id = st.selectbox(
            "Estado",
            options=list(estado_map.keys()),
            format_func=lambda x: estado_map[x],
            key="c_estado",
        )
        cidades = _get_cidades(estado_id)
        cidade_map = {c["cidade_id"]: c["descricao"] for c in cidades}
        cidade_id = st.selectbox(
            "Cidade",
            options=list(cidade_map.keys()),
            format_func=lambda x: cidade_map.get(x, str(x)),
            key=f"c_cidade_{estado_id}",
        )

    if st.button("Criar", key="c_submit"):
        payload = {
            "nome": nome,
            "email": email,
            "telefone": telefone,
            "endereco": endereco,
            "data_nascimento": data_nascimento.isoformat(),
            "cidade_id": cidade_id,
        }
        result = api.create_cliente(payload)
        if "cliente_id" in result:
            st.success(f"Cliente #{result['cliente_id']} criado com sucesso.")
            st.rerun(scope="app")
        else:
            st.error(f"Erro: {result}")


with st.expander("Criar novo cliente"):
    _criar_cliente()


# --- Editar ---
@st.fragment
def _editar_cliente(data):
    ids = [r["cliente_id"] for r in data]
    selected_id = st.selectbox(
        "Selecione o cliente",
        ids,
        format_func=lambda x: next(r["nome"] for r in data if r["cliente_id"] == x),
        key="edit_cliente_sel",
    )
    record = next(r for r in data if r["cliente_id"] == selected_id)

    estados = _get_estados()
    estado_map = {e["estado_id"]: f"{e['uf']} — {e['descricao']}" for e in estados}
    estado_keys = list(estado_map.keys())
    cur_estado = (
        record["cidade"]["estado"]["estado_id"]
        if isinstance(record.get("cidade"), dict)
        else estado_keys[0]
    )

    col1, col2 = st.columns(2)
    with col1:
        new_nome = st.text_input(
            "Nome", value=record.get("nome", ""), key=f"e_nome_{selected_id}"
        )
        new_email = st.text_input(
            "E-mail", value=record.get("email", ""), key=f"e_email_{selected_id}"
        )
        new_telefone = st.text_input(
            "Telefone", value=record.get("telefone", ""), key=f"e_tel_{selected_id}"
        )
    with col2:
        new_endereco = st.text_input(
            "Endereço", value=record.get("endereco", ""), key=f"e_end_{selected_id}"
        )
        new_estado = st.selectbox(
            "Estado",
            options=estado_keys,
            index=estado_keys.index(cur_estado) if cur_estado in estado_keys else 0,
            format_func=lambda x: estado_map[x],
            key=f"e_estado_{selected_id}",
        )
        cidades = _get_cidades(new_estado)
        cidade_map = {c["cidade_id"]: c["descricao"] for c in cidades}
        cidade_keys = list(cidade_map.keys())
        cur_cidade = (
            record["cidade"]["cidade_id"]
            if isinstance(record.get("cidade"), dict)
            else cidade_keys[0] if cidade_keys else None
        )
        new_cidade = st.selectbox(
            "Cidade",
            options=cidade_keys,
            index=cidade_keys.index(cur_cidade) if cur_cidade in cidade_keys else 0,
            format_func=lambda x: cidade_map.get(x, str(x)),
            key=f"e_cidade_{selected_id}_{new_estado}",
        )

    if st.button("Salvar alterações", key="e_submit"):
        result = api.update_cliente(
            selected_id,
            {
                "nome": new_nome,
                "email": new_email,
                "telefone": new_telefone,
                "endereco": new_endereco,
                "cidade_id": new_cidade,
            },
        )
        if "cliente_id" in result:
            st.success("Cliente atualizado.")
            st.rerun(scope="app")
        else:
            st.error(f"Erro: {result}")


st.subheader("Editar cliente")
if data:
    _editar_cliente(data)
