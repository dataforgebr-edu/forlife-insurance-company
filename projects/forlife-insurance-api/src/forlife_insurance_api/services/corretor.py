from forlife_insurance_api.schemas.corretor import CorretorCreate, CorretorUpdate
from forlife_insurance_core.models.corretor import Corretor
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


def _corretor_options():
    return (selectinload(Corretor.estado),)


def get_corretores(db: Session, skip: int, limit: int):
    stmt = (
        select(Corretor)
        .options(*_corretor_options())
        .offset(skip)
        .limit(limit)
        .order_by(Corretor.corretor_id)
    )
    return db.scalars(stmt).all()


def get_corretor(db: Session, corretor_id: int):
    stmt = (
        select(Corretor)
        .options(*_corretor_options())
        .where(Corretor.corretor_id == corretor_id)
    )
    return db.scalars(stmt).first()


def create_corretor(db: Session, data: CorretorCreate) -> Corretor:
    corretor = Corretor(**data.model_dump())
    db.add(corretor)
    db.commit()
    return get_corretor(db, corretor.corretor_id)


def update_corretor(db: Session, corretor_id: int, data: CorretorUpdate):
    corretor = db.get(Corretor, corretor_id)
    if corretor is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(corretor, key, value)
    db.commit()
    return get_corretor(db, corretor_id)
