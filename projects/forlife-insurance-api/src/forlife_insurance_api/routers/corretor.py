from fastapi import APIRouter, Depends, HTTPException, Path, status
from forlife_insurance_api.schemas.corretor import (
    CorretorCreate,
    CorretorResponse,
    CorretorUpdate,
)
from forlife_insurance_api.services.corretor import (
    create_corretor,
    delete_corretor,
    get_corretor,
    get_corretores,
    update_corretor,
)
from forlife_insurance_core.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/corretores", tags=["corretores"])


@router.get("", response_model=list[CorretorResponse])
def list_corretores_endpoint(
    db: Session = Depends(get_db), skip: int = 0, limit: int = 10
):
    return get_corretores(db, skip, limit)


@router.get("/{corretor_id}", response_model=CorretorResponse)
def get_corretor_endpoint(
    corretor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    corretor = get_corretor(db, corretor_id)
    if corretor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Corretor não encontrado."
        )
    return corretor


@router.post("", response_model=CorretorResponse, status_code=status.HTTP_201_CREATED)
def create_corretor_endpoint(data: CorretorCreate, db: Session = Depends(get_db)):
    return create_corretor(db, data)


@router.put("/{corretor_id}", response_model=CorretorResponse)
def update_corretor_endpoint(
    data: CorretorUpdate,
    corretor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    corretor = update_corretor(db, corretor_id, data)
    if corretor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Corretor não encontrado."
        )
    return corretor


@router.delete("/{corretor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_corretor_endpoint(
    corretor_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
):
    if not delete_corretor(db, corretor_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Corretor não encontrado."
        )
