from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .cliente import ClienteResponse
from .corretor import CorretorResponse
from .dominios import (
    MeioPagamentoResponse,
    PeriodicidadePagamentoResponse,
    ProdutoResponse,
    StatusApoliceResponse,
)


class ApoliceBase(BaseModel):
    capital_segurado: float
    premio: float
    inicio_vigencia: datetime
    fim_vigencia: datetime


class ApoliceResponse(ApoliceBase):
    apolice_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    status_apolice: StatusApoliceResponse
    periodicidade_pagamento: PeriodicidadePagamentoResponse
    produto: ProdutoResponse
    meio_pagamento: MeioPagamentoResponse
    cliente: ClienteResponse
    corretor: CorretorResponse

    model_config = ConfigDict(from_attributes=True)


class ApoliceCreate(ApoliceBase):
    pass


class ApoliceUpdate(BaseModel):
    pass
