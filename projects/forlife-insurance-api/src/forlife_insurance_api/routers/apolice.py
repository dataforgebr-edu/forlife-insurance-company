from fastapi import APIRouter, Depends, HTTPException, Path, status
from forlife_insurance_api.schemas.apolice import (
    ApoliceCreate,
    ApoliceResponse,
    ApoliceSumaryResponse,
    ApoliceUpdate,
)
from forlife_insurance_api.services.apolice import (
    create_apolice,
    delete_apolice,
    get_apolice,
    get_apolices,
    update_apolice,
)
from forlife_insurance_core.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/apolices", tags=["apolices"])


@router.get("", response_model=list[ApoliceSumaryResponse])
def list_apolices_endpoint(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
):
    return get_apolices(db, skip, limit)


@router.get("/{apolice_id}", response_model=ApoliceResponse)
def get_apolice_endpoint(
    apolice_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    apolice = get_apolice(db, apolice_id)
    if apolice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Apólice não encontrada."
        )
    return apolice


@router.post(
    "", response_model=ApoliceSumaryResponse, status_code=status.HTTP_201_CREATED
)
def create_apolice_endpoint(data: ApoliceCreate, db: Session = Depends(get_db)):
    return create_apolice(db, data)


@router.put("/{apolice_id}", response_model=ApoliceSumaryResponse)
def update_apolice_endpoint(
    data: ApoliceUpdate,
    apolice_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    apolice = update_apolice(db, apolice_id, data)
    if apolice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Apólice não encontrada."
        )
    return apolice


@router.delete("/{apolice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_apolice_endpoint(
    apolice_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    if not delete_apolice(db, apolice_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Apólice não encontrada."
        )
