from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from forlife_insurance_api.schemas.parcelas import (
    ParcelaCreate,
    ParcelaResponse,
    ParcelaUpdate,
)
from forlife_insurance_api.services.parcelas import (
    create_parcela,
    get_parcela,
    get_parcelas,
    update_parcela,
)
from forlife_insurance_core.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/parcelas", tags=["parcelas"])


@router.get("", response_model=list[ParcelaResponse])
def list_parcelas_endpoint(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    apolice_id: int | None = Query(default=None, ge=1),
):
    return get_parcelas(db, skip, limit, apolice_id)


@router.get("/{parcela_id}", response_model=ParcelaResponse)
def get_parcela_endpoint(
    parcela_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    parcela = get_parcela(db, parcela_id)
    if parcela is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parcela não encontrada."
        )
    return parcela


@router.post("", response_model=ParcelaResponse, status_code=status.HTTP_201_CREATED)
def create_parcela_endpoint(data: ParcelaCreate, db: Session = Depends(get_db)):
    return create_parcela(db, data)


@router.put("/{parcela_id}", response_model=ParcelaResponse)
def update_parcela_endpoint(
    data: ParcelaUpdate,
    parcela_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    parcela = update_parcela(db, parcela_id, data)
    if parcela is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Parcela não encontrada."
        )
    return parcela
