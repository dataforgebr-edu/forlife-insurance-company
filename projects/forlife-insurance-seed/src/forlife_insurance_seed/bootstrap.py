from __future__ import annotations

from forlife_insurance_core.models.dominios import (
    Cidade,
    Estado,
    MeioPagamento,
    PeriodicidadePagamento,
    Produto,
    StatusApolice,
    StatusSinistro,
)
from forlife_insurance_seed.types import DomainReferences
from sqlalchemy import select
from sqlalchemy.orm import Session

PERIODICIDADE_MESES = {
    "Mensal": 1,
    "Trimestral": 3,
    "Semestral": 6,
    "Anual": 12,
}


def _insert_if_empty(session: Session, items: list[object], pk_column) -> None:
    if not session.scalar(select(pk_column).limit(1)):
        session.add_all(items)
        session.flush()


def bootstrap_domain_data(session: Session) -> None:
    _insert_if_empty(
        session,
        [
            Estado(uf="SP", descricao="Sao Paulo"),
            Estado(uf="RJ", descricao="Rio de Janeiro"),
            Estado(uf="MG", descricao="Minas Gerais"),
            Estado(uf="PR", descricao="Parana"),
            Estado(uf="RS", descricao="Rio Grande do Sul"),
            Estado(uf="BA", descricao="Bahia"),
        ],
        Estado.estado_id,
    )

    if not session.scalar(select(Cidade.cidade_id).limit(1)):
        cidades_por_uf = {
            "SP": ["Sao Paulo", "Campinas", "Santos", "Sorocaba"],
            "RJ": ["Rio de Janeiro", "Niteroi", "Petropolis", "Volta Redonda"],
            "MG": ["Belo Horizonte", "Uberlandia", "Contagem", "Juiz de Fora"],
            "PR": ["Curitiba", "Londrina", "Maringa", "Ponta Grossa"],
            "RS": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Santa Maria"],
            "BA": ["Salvador", "Feira de Santana", "Vitoria da Conquista", "Ilheus"],
        }
        estado_ids_por_uf = {
            uf: estado_id
            for estado_id, uf in session.execute(
                select(Estado.estado_id, Estado.uf)
            ).all()
        }
        session.add_all(
            [
                Cidade(descricao=cidade, estado_id=estado_ids_por_uf[uf])
                for uf, cidades in cidades_por_uf.items()
                for cidade in cidades
                if uf in estado_ids_por_uf
            ]
        )
        session.flush()

    _insert_if_empty(
        session,
        [
            Produto(descricao="Seguro de Vida"),
            Produto(descricao="Seguro Auto"),
            Produto(descricao="Seguro Residencial"),
        ],
        Produto.produto_id,
    )

    _insert_if_empty(
        session,
        [
            StatusApolice(descricao="Ativa"),
            StatusApolice(descricao="Cancelada"),
            StatusApolice(descricao="Vencida"),
        ],
        StatusApolice.status_apolice_id,
    )

    _insert_if_empty(
        session,
        [
            PeriodicidadePagamento(descricao="Mensal"),
            PeriodicidadePagamento(descricao="Trimestral"),
            PeriodicidadePagamento(descricao="Semestral"),
            PeriodicidadePagamento(descricao="Anual"),
        ],
        PeriodicidadePagamento.periodicidade_id,
    )

    _insert_if_empty(
        session,
        [
            MeioPagamento(descricao="Cartao de Credito"),
            MeioPagamento(descricao="Boleto"),
            MeioPagamento(descricao="Debito em Conta"),
            MeioPagamento(descricao="Pix"),
        ],
        MeioPagamento.meio_pagamento_id,
    )

    _insert_if_empty(
        session,
        [
            StatusSinistro(descricao="Avisado"),
            StatusSinistro(descricao="Em Analise"),
            StatusSinistro(descricao="Pago"),
        ],
        StatusSinistro.status_sinistro_id,
    )

    session.commit()


def load_domain_references(session: Session) -> DomainReferences:
    periodicidade_por_descricao = {
        descricao: periodicidade_id
        for periodicidade_id, descricao in session.execute(
            select(
                PeriodicidadePagamento.periodicidade_id,
                PeriodicidadePagamento.descricao,
            )
        ).all()
    }
    return DomainReferences(
        estado_ids=session.scalars(select(Estado.estado_id)).all(),
        cidade_ids=session.scalars(select(Cidade.cidade_id)).all(),
        produto_ids=session.scalars(select(Produto.produto_id)).all(),
        status_apolice_ids=session.scalars(
            select(StatusApolice.status_apolice_id)
        ).all(),
        periodicidade_por_descricao=periodicidade_por_descricao,
        meio_pagamento_ids=session.scalars(
            select(MeioPagamento.meio_pagamento_id)
        ).all(),
        status_sinistro_ids=session.scalars(
            select(StatusSinistro.status_sinistro_id)
        ).all(),
    )
