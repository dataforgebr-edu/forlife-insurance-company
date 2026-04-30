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


def get_apolices(db: Session):
    stmt = select(Apolice).options(*_apolice_options()).order_by(Apolice.apolice_id)
    return db.scalars(stmt).all()


def get_apolice(db: Session, apolice_id: int):
    stmt = (
        select(Apolice)
        .options(*_apolice_options())
        .where(Apolice.apolice_id == apolice_id)
    )
    return db.scalars(stmt).first()
