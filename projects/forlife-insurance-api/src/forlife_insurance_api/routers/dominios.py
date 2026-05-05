from fastapi import APIRouter, Depends, Query
from forlife_insurance_api.schemas.dominios import (
    CidadeResponse,
    EstadoResponse,
    MeioPagamentoResponse,
    PeriodicidadePagamentoResponse,
    ProdutoResponse,
    StatusApoliceResponse,
    StatusSinistroResponse,
)
from forlife_insurance_api.services.dominios import (
    get_cidades,
    get_estados,
    get_meios_pagamento,
    get_periodicidades,
    get_produtos,
    get_status_apolice,
    get_status_sinistro,
)
from forlife_insurance_core.database.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/dominios", tags=["dominios"])


@router.get("/estados", response_model=list[EstadoResponse])
def list_estados_endpoint(db: Session = Depends(get_db)):
    return get_estados(db)


@router.get("/cidades", response_model=list[CidadeResponse])
def list_cidades_endpoint(
    db: Session = Depends(get_db),
    estado_id: int | None = Query(default=None, ge=1),
):
    return get_cidades(db, estado_id)


@router.get("/produtos", response_model=list[ProdutoResponse])
def list_produtos_endpoint(db: Session = Depends(get_db)):
    return get_produtos(db)


@router.get("/status-apolice", response_model=list[StatusApoliceResponse])
def list_status_apolice_endpoint(db: Session = Depends(get_db)):
    return get_status_apolice(db)


@router.get("/periodicidades", response_model=list[PeriodicidadePagamentoResponse])
def list_periodicidades_endpoint(db: Session = Depends(get_db)):
    return get_periodicidades(db)


@router.get("/meios-pagamento", response_model=list[MeioPagamentoResponse])
def list_meios_pagamento_endpoint(db: Session = Depends(get_db)):
    return get_meios_pagamento(db)


@router.get("/status-sinistro", response_model=list[StatusSinistroResponse])
def list_status_sinistro_endpoint(db: Session = Depends(get_db)):
    return get_status_sinistro(db)
