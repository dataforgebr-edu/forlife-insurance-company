from datetime import datetime
from typing import Optional

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


class ApoliceSumaryResponse(ApoliceBase):
    apolice_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    cliente_id: int
    corretor_id: int
    status_apolice: StatusApoliceResponse
    periodicidade_pagamento: PeriodicidadePagamentoResponse
    produto: ProdutoResponse
    meio_pagamento: MeioPagamentoResponse

    model_config = ConfigDict(from_attributes=True)


class ApoliceCreate(ApoliceBase):
    cliente_id: int
    corretor_id: int
    produto_id: int
    status_apolice_id: int
    periodicidade_id: int
    meio_pagamento_id: int


class ApoliceUpdate(BaseModel):
    capital_segurado: Optional[float] = None
    premio: Optional[float] = None
    inicio_vigencia: Optional[datetime] = None
    fim_vigencia: Optional[datetime] = None
    cliente_id: Optional[int] = None
    corretor_id: Optional[int] = None
    produto_id: Optional[int] = None
    status_apolice_id: Optional[int] = None
    periodicidade_id: Optional[int] = None
    meio_pagamento_id: Optional[int] = None
