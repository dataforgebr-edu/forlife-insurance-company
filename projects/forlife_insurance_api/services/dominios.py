from forlife_insurance_core.models.dominios import (
    Cidade,
    Estado,
    MeioPagamento,
    PeriodicidadePagamento,
    Produto,
    StatusApolice,
    StatusSinistro,
)
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


def get_estados(db: Session):
    return db.scalars(select(Estado).order_by(Estado.uf)).all()


def get_cidades(db: Session, estado_id: int | None = None):
    stmt = (
        select(Cidade).options(selectinload(Cidade.estado)).order_by(Cidade.descricao)
    )
    if estado_id is not None:
        stmt = stmt.where(Cidade.estado_id == estado_id)
    return db.scalars(stmt).all()


def get_produtos(db: Session):
    return db.scalars(select(Produto).order_by(Produto.descricao)).all()


def get_status_apolice(db: Session):
    return db.scalars(select(StatusApolice).order_by(StatusApolice.descricao)).all()


def get_periodicidades(db: Session):
    return db.scalars(
        select(PeriodicidadePagamento).order_by(PeriodicidadePagamento.descricao)
    ).all()


def get_meios_pagamento(db: Session):
    return db.scalars(select(MeioPagamento).order_by(MeioPagamento.descricao)).all()


def get_status_sinistro(db: Session):
    return db.scalars(select(StatusSinistro).order_by(StatusSinistro.descricao)).all()
