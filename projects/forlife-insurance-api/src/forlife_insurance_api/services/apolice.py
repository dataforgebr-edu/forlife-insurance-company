from forlife_insurance_api.schemas.apolice import ApoliceCreate, ApoliceUpdate
from forlife_insurance_core.models.apolice import Apolice
from forlife_insurance_core.models.cliente import Cliente
from forlife_insurance_core.models.corretor import Corretor
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


def _apolice_options():
    return (
        selectinload(Apolice.status_apolice),
        selectinload(Apolice.periodicidade_pagamento),
        selectinload(Apolice.produto),
        selectinload(Apolice.meio_pagamento),
        selectinload(Apolice.cliente).selectinload(Cliente.cidade),
        selectinload(Apolice.corretor).selectinload(Corretor.estado),
    )


def get_apolices(db: Session, skip: int, limit: int):
    stmt = (
        select(Apolice)
        .options(*_apolice_options())
        .offset(skip)
        .limit(limit)
        .order_by(Apolice.apolice_id)
    )
    return db.scalars(stmt).all()


def get_apolice(db: Session, apolice_id: int):
    stmt = (
        select(Apolice)
        .options(*_apolice_options())
        .where(Apolice.apolice_id == apolice_id)
    )
    return db.scalars(stmt).first()


def create_apolice(db: Session, data: ApoliceCreate) -> Apolice:
    apolice = Apolice(**data.model_dump())
    db.add(apolice)
    db.commit()
    return get_apolice(db, apolice.apolice_id)


def update_apolice(db: Session, apolice_id: int, data: ApoliceUpdate):
    apolice = db.get(Apolice, apolice_id)
    if apolice is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(apolice, key, value)
    db.commit()
    return get_apolice(db, apolice_id)


def delete_apolice(db: Session, apolice_id: int) -> bool:
    apolice = db.get(Apolice, apolice_id)
    if apolice is None:
        return False
    db.delete(apolice)
    db.commit()
    return True
