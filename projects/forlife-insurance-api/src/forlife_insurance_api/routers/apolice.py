from fastapi import APIRouter, Depends, HTTPException, Path, status
from forlife_insurance_api.schemas.apolice import ApoliceResponse
from forlife_insurance_api.services.apolice import get_apolice, get_apolices
from forlife_insurance_core.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/apolices", tags=["apolices"])


@router.get("", response_model=list[ApoliceResponse])
def list_apolices_endpoint(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
) -> list[ApoliceResponse]:
    return get_apolices(db, skip, limit)


@router.get("/{apolice_id}", response_model=ApoliceResponse)
def get_apolice_endpoint(
    apolice_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
) -> ApoliceResponse:
    apolice = get_apolice(db, apolice_id)
    if apolice is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Apólice não encontrada.",
        )
    return apolice
