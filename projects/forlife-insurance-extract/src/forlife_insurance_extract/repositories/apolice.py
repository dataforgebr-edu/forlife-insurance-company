from collections.abc import Iterator
from datetime import datetime

from forlife_insurance_core.models.apolice import Apolice
from forlife_insurance_core.models.cliente import Cliente
from forlife_insurance_core.models.corretor import Corretor
from forlife_insurance_core.models.dominios import (
    Cidade,
    Estado,
    MeioPagamento,
    PeriodicidadePagamento,
    Produto,
    StatusApolice,
)
from forlife_insurance_extract.schemas.apolice import ApoliceExtractRow
from sqlalchemy import Select, select
from sqlalchemy.orm import Session


def build_apolice_extract_stmt(
    *,
    changed_since: datetime | None = None,
    last_apolice_id: int | None = None,
    limit: int | None = None,
) -> Select:
    """Monta uma query plana e incremental para extração de apólices."""

    stmt = (
        select(
            Apolice.apolice_id.label("apolice_id"),
            Apolice.capital_segurado.label("capital_segurado"),
            Apolice.premio.label("premio"),
            Apolice.inicio_vigencia.label("inicio_vigencia"),
            Apolice.fim_vigencia.label("fim_vigencia"),
            Apolice.data_insercao.label("data_insercao"),
            Apolice.data_atualizacao.label("data_atualizacao"),
            Apolice.status_apolice_id.label("status_apolice_id"),
            StatusApolice.descricao.label("status_apolice_descricao"),
            Apolice.periodicidade_id.label("periodicidade_id"),
            PeriodicidadePagamento.descricao.label("periodicidade_descricao"),
            Apolice.produto_id.label("produto_id"),
            Produto.descricao.label("produto_descricao"),
            Apolice.meio_pagamento_id.label("meio_pagamento_id"),
            MeioPagamento.descricao.label("meio_pagamento_descricao"),
            Apolice.corretor_id.label("corretor_id"),
            Corretor.nome.label("corretor_nome"),
            Corretor.cnpj.label("corretor_cnpj"),
            Corretor.email.label("corretor_email"),
            Apolice.cliente_id.label("cliente_id"),
            Cliente.nome.label("cliente_nome"),
            Cliente.email.label("cliente_email"),
            Cliente.telefone.label("cliente_telefone"),
            Cliente.endereco.label("cliente_endereco"),
            Cliente.data_nascimento.label("cliente_data_nascimento"),
            Cliente.cidade_id.label("cidade_id"),
            Cidade.descricao.label("cidade_descricao"),
            Estado.estado_id.label("estado_id"),
            Estado.uf.label("estado_uf"),
            Estado.descricao.label("estado_descricao"),
        )
        .join(
            StatusApolice,
            StatusApolice.status_apolice_id == Apolice.status_apolice_id,
        )
        .join(
            PeriodicidadePagamento,
            PeriodicidadePagamento.periodicidade_id == Apolice.periodicidade_id,
        )
        .join(Produto, Produto.produto_id == Apolice.produto_id)
        .join(
            MeioPagamento, MeioPagamento.meio_pagamento_id == Apolice.meio_pagamento_id
        )
        .join(Corretor, Corretor.corretor_id == Apolice.corretor_id)
        .join(Cliente, Cliente.cliente_id == Apolice.cliente_id)
        .join(Cidade, Cidade.cidade_id == Cliente.cidade_id)
        .join(Estado, Estado.estado_id == Cidade.estado_id)
        .order_by(Apolice.data_atualizacao, Apolice.apolice_id)
    )

    if changed_since is not None:
        stmt = stmt.where(Apolice.data_atualizacao > changed_since)

    if last_apolice_id is not None:
        stmt = stmt.where(Apolice.apolice_id > last_apolice_id)

    if limit is not None:
        stmt = stmt.limit(limit)

    return stmt


def list_apolices_extract(
    db: Session,
    *,
    changed_since: datetime | None = None,
    last_apolice_id: int | None = None,
    limit: int | None = None,
) -> list[ApoliceExtractRow]:
    """Retorna apólices já prontas para serialização em lote."""

    stmt = build_apolice_extract_stmt(
        changed_since=changed_since,
        last_apolice_id=last_apolice_id,
        limit=limit,
    )
    return [
        ApoliceExtractRow.model_validate(row) for row in db.execute(stmt).mappings()
    ]


def iter_apolices_extract(
    db: Session,
    *,
    changed_since: datetime | None = None,
    last_apolice_id: int | None = None,
    limit: int | None = None,
) -> Iterator[ApoliceExtractRow]:
    """Itera linhas de apólice sem carregar tudo em memória."""

    stmt = build_apolice_extract_stmt(
        changed_since=changed_since,
        last_apolice_id=last_apolice_id,
        limit=limit,
    ).execution_options(stream_results=True)

    for row in db.execute(stmt).mappings():
        yield ApoliceExtractRow.model_validate(row)
