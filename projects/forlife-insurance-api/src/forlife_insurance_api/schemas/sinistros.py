from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveFloat

from .apolice import ApoliceResponse
from .dominios import MeioPagamentoResponse, StatusSinistroResponse


class SinistroBase(BaseModel):
    valor: PositiveFloat
    data_pagamento: datetime


class SinistroResponse(SinistroBase):
    data_insercao: datetime
    data_atualizacao: datetime
    status_sinistro: StatusSinistroResponse
    meio_pagamento: MeioPagamentoResponse
    apolice: ApoliceResponse

    model_config = ConfigDict(from_attributes=True)


class SinistroSummaryResponse(SinistroBase):
    data_insercao: datetime
    data_atualizacao: datetime
    status_sinistro: StatusSinistroResponse
    meio_pagamento: MeioPagamentoResponse
    apolice_id: int

    model_config = ConfigDict(from_attributes=True)


class SinistroCreate(SinistroBase):
    pass


class SinistroUpdate(BaseModel):
    pass
