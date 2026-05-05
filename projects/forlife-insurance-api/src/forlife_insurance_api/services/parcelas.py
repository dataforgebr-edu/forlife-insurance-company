from forlife_insurance_api.schemas.parcelas import ParcelaCreate, ParcelaUpdate
from forlife_insurance_core.models.parcelas import Parcela
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


def _parcela_options():
    return (selectinload(Parcela.meio_pagamento),)


def get_parcelas(db: Session, skip: int, limit: int, apolice_id: int | None = None):
    stmt = (
        select(Parcela)
        .options(*_parcela_options())
        .offset(skip)
        .limit(limit)
        .order_by(Parcela.parcela_id)
    )
    if apolice_id is not None:
        stmt = stmt.where(Parcela.apolice_id == apolice_id)
    return db.scalars(stmt).all()


def get_parcela(db: Session, parcela_id: int):
    stmt = (
        select(Parcela)
        .options(*_parcela_options())
        .where(Parcela.parcela_id == parcela_id)
    )
    return db.scalars(stmt).first()


def create_parcela(db: Session, data: ParcelaCreate) -> Parcela:
    parcela = Parcela(**data.model_dump())
    db.add(parcela)
    db.commit()
    return get_parcela(db, parcela.parcela_id)


def update_parcela(db: Session, parcela_id: int, data: ParcelaUpdate):
    parcela = db.get(Parcela, parcela_id)
    if parcela is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(parcela, key, value)
    db.commit()
    return get_parcela(db, parcela_id)


def delete_parcela(db: Session, parcela_id: int) -> bool:
    parcela = db.get(Parcela, parcela_id)
    if parcela is None:
        return False
    db.delete(parcela)
    db.commit()
    return True
