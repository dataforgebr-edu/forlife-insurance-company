from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.dominios import (
    Cidade,
    Estados,
    EstatusApolice,
    EstatusSinistro,
    MeioPagamento,
    PeriodicidadePagamento,
    Produtos,
)
from seed.types import DomainReferences

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
            Estados(uf="SP", descricao="Sao Paulo"),
            Estados(uf="RJ", descricao="Rio de Janeiro"),
            Estados(uf="MG", descricao="Minas Gerais"),
            Estados(uf="PR", descricao="Parana"),
            Estados(uf="RS", descricao="Rio Grande do Sul"),
            Estados(uf="BA", descricao="Bahia"),
        ],
        Estados.estado_id,
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
                select(Estados.estado_id, Estados.uf)
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
            Produtos(descricao="Seguro de Vida"),
            Produtos(descricao="Seguro Auto"),
            Produtos(descricao="Seguro Residencial"),
        ],
        Produtos.produto_id,
    )

    _insert_if_empty(
        session,
        [
            EstatusApolice(descricao="Ativa"),
            EstatusApolice(descricao="Cancelada"),
            EstatusApolice(descricao="Vencida"),
        ],
        EstatusApolice.estatus_apolice_id,
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
            EstatusSinistro(descricao="Avisado"),
            EstatusSinistro(descricao="Em Analise"),
            EstatusSinistro(descricao="Pago"),
        ],
        EstatusSinistro.estatus_sinistro_id,
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
        estado_ids=session.scalars(select(Estados.estado_id)).all(),
        cidade_ids=session.scalars(select(Cidade.cidade_id)).all(),
        produto_ids=session.scalars(select(Produtos.produto_id)).all(),
        estatus_apolice_ids=session.scalars(
            select(EstatusApolice.estatus_apolice_id)
        ).all(),
        periodicidade_por_descricao=periodicidade_por_descricao,
        meio_pagamento_ids=session.scalars(
            select(MeioPagamento.meio_pagamento_id)
        ).all(),
        estatus_sinistro_ids=session.scalars(
            select(EstatusSinistro.estatus_sinistro_id)
        ).all(),
    )
