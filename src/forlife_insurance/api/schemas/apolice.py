from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .cliente import ClienteResponse
from .corretor import CorretorResponse
from .dominios import (
    EstatusApoliceReponse,
    MeioPagamentoReponse,
    PeriodicidadePagamentoReponse,
    ProdutoReponse,
)


class ApoliceBase(BaseModel):
    capital_segurado: float
    premio: float
    inicio_vigencia: datetime
    fim_vigencia: datetime


class ApoliceReponse(ApoliceBase):
    apolice_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    estatus_apolice: EstatusApoliceReponse
    periodicidade_pagamento: PeriodicidadePagamentoReponse
    produtos: ProdutoReponse
    meio_pagamento: MeioPagamentoReponse
    cliente: ClienteResponse
    corretor: CorretorResponse

    model_config = ConfigDict(from_attributes=True)


class ApoliceCreate(ApoliceBase):
    pass


class ApoliceUpdate(BaseModel):
    pass
