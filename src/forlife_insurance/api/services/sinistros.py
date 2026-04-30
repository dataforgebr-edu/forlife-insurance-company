from sqlalchemy import select
from sqlalchemy.orm import Session

from forlife_insurance.models.sinistros import Sinistro


def get_sinistros(db: Session):
    return db.scalars(select(Sinistro)).all()


def get_sinistro(db: Session, sinistro_id: int):
    return db.scalars(
        select(Sinistro).where(Sinistro.sinistro_id == sinistro_id)
    ).first()
