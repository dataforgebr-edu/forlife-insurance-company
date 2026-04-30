from sqlalchemy import select
from sqlalchemy.orm import Session

from forlife_insurance.models.sinistros import Sinistros


def get_sinistros(db: Session):
    return db.scalars(select(Sinistros)).all()


def get_sinistro(db: Session, sinistro_id: int):
    return db.scalars(
        select(Sinistros).where(Sinistros.sinistro_id == sinistro_id)
    ).first()
