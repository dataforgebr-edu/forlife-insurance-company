from sqlalchemy import select
from sqlalchemy.orm import Session

from forlife_insurance.models.apolice import Apolice


def get_apolices(db: Session):
    return db.scalars(select(Apolice)).all()


def get_apolice(db: Session, apolice_id: int):
    return db.scalars(select(Apolice).where(Apolice.apolice_id == apolice_id)).first()
