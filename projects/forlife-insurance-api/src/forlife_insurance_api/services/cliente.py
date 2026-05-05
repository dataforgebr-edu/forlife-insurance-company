from forlife_insurance_api.schemas.cliente import ClienteCreate, ClienteUpdate
from forlife_insurance_core.models.cliente import Cliente
from forlife_insurance_core.models.dominios import Cidade
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


def _cliente_options():
    return (selectinload(Cliente.cidade).selectinload(Cidade.estado),)


def get_clientes(db: Session, skip: int, limit: int):
    stmt = (
        select(Cliente)
        .options(*_cliente_options())
        .offset(skip)
        .limit(limit)
        .order_by(Cliente.cliente_id)
    )
    return db.scalars(stmt).all()


def get_cliente(db: Session, cliente_id: int):
    stmt = (
        select(Cliente)
        .options(*_cliente_options())
        .where(Cliente.cliente_id == cliente_id)
    )
    return db.scalars(stmt).first()


def create_cliente(db: Session, data: ClienteCreate) -> Cliente:
    cliente = Cliente(**data.model_dump())
    db.add(cliente)
    db.commit()
    return get_cliente(db, cliente.cliente_id)


def update_cliente(db: Session, cliente_id: int, data: ClienteUpdate):
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(cliente, key, value)
    db.commit()
    return get_cliente(db, cliente_id)


def delete_cliente(db: Session, cliente_id: int) -> bool:
    cliente = db.get(Cliente, cliente_id)
    if cliente is None:
        return False
    db.delete(cliente)
    db.commit()
    return True
