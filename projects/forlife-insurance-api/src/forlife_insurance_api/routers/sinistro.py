from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from forlife_insurance_api.schemas.sinistros import (
    SinistroCreate,
    SinistroResponse,
    SinistroUpdate,
)
from forlife_insurance_api.services.sinistros import (
    create_sinistro,
    get_sinistro,
    get_sinistros,
    update_sinistro,
)
from forlife_insurance_core.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/sinistros", tags=["sinistros"])


@router.get("", response_model=list[SinistroResponse])
def list_sinistros_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    apolice_id: int | None = Query(default=None, ge=1),
):
    return get_sinistros(db, skip, limit, apolice_id)


@router.get("/{sinistro_id}", response_model=SinistroResponse)
def get_sinistro_endpoint(
    sinistro_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    sinistro = get_sinistro(db, sinistro_id)
    if sinistro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sinistro não encontrado."
        )
    return sinistro


@router.post("", response_model=SinistroResponse, status_code=status.HTTP_201_CREATED)
def create_sinistro_endpoint(data: SinistroCreate, db: Session = Depends(get_db)):
    return create_sinistro(db, data)


@router.put("/{sinistro_id}", response_model=SinistroResponse)
def update_sinistro_endpoint(
    data: SinistroUpdate,
    sinistro_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    sinistro = update_sinistro(db, sinistro_id, data)
    if sinistro is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sinistro não encontrado."
        )
    return sinistro
