from forlife_insurance_api.schemas.sinistros import SinistroCreate, SinistroUpdate
from forlife_insurance_core.models.sinistros import Sinistro
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


def _sinistros_options():
    return (
        selectinload(Sinistro.status_sinistro),
        selectinload(Sinistro.meio_pagamento),
    )


def get_sinistros(db: Session, skip: int, limit: int, apolice_id: int | None = None):
    stmt = (
        select(Sinistro)
        .options(*_sinistros_options())
        .offset(skip)
        .limit(limit)
        .order_by(Sinistro.sinistro_id)
    )
    if apolice_id is not None:
        stmt = stmt.where(Sinistro.apolice_id == apolice_id)
    return db.scalars(stmt).all()


def get_sinistro(db: Session, sinistro_id: int):
    stmt = (
        select(Sinistro)
        .options(*_sinistros_options())
        .where(Sinistro.sinistro_id == sinistro_id)
    )
    return db.scalars(stmt).first()


def create_sinistro(db: Session, data: SinistroCreate) -> Sinistro:
    sinistro = Sinistro(**data.model_dump())
    db.add(sinistro)
    db.commit()
    return get_sinistro(db, sinistro.sinistro_id)


def update_sinistro(db: Session, sinistro_id: int, data: SinistroUpdate):
    sinistro = db.get(Sinistro, sinistro_id)
    if sinistro is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sinistro, key, value)
    db.commit()
    return get_sinistro(db, sinistro_id)


def delete_sinistro(db: Session, sinistro_id: int) -> bool:
    sinistro = db.get(Sinistro, sinistro_id)
    if sinistro is None:
        return False
    db.delete(sinistro)
    db.commit()
    return True
