from fastapi import APIRouter, Depends, HTTPException, Path, status
from forlife_insurance_api.schemas.cliente import (
    ClienteCreate,
    ClienteResponse,
    ClienteUpdate,
)
from forlife_insurance_api.services.cliente import (
    create_cliente,
    delete_cliente,
    get_cliente,
    get_clientes,
    update_cliente,
)
from forlife_insurance_core.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.get("", response_model=list[ClienteResponse])
def list_clientes_endpoint(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
):
    return get_clientes(db, skip, limit)


@router.get("/{cliente_id}", response_model=ClienteResponse)
def get_cliente_endpoint(
    cliente_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    cliente = get_cliente(db, cliente_id)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
    return cliente


@router.post("", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def create_cliente_endpoint(data: ClienteCreate, db: Session = Depends(get_db)):
    return create_cliente(db, data)


@router.put("/{cliente_id}", response_model=ClienteResponse)
def update_cliente_endpoint(
    data: ClienteUpdate,
    cliente_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    cliente = update_cliente(db, cliente_id, data)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
    return cliente


@router.delete("/{cliente_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_cliente_endpoint(
    cliente_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    if not delete_cliente(db, cliente_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado."
        )
