from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveFloat

from .apolice import ApoliceResponse
from .dominios import MeioPagamentoResponse


class ParcelaBase(BaseModel):
    valor: PositiveFloat
    data_emissao: datetime
    data_periodo: datetime
    data_pagamento: datetime


class ParcelaResponse(ParcelaBase):
    parcela_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    apolice: ApoliceResponse
    meio_pagamento: MeioPagamentoResponse

    model_config = ConfigDict(from_attributes=True)


class ParcelaSummaryResponse(ParcelaBase):
    parcela_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    apolice_id: int
    meio_pagamento: MeioPagamentoResponse

    model_config = ConfigDict(from_attributes=True)


class ParcelaCreate(ParcelaBase):
    pass


class ParcelaUpdate(BaseModel):
    pass
