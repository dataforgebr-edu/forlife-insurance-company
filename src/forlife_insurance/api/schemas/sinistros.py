from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveFloat

from .apolice import ApoliceReponse
from .dominios import EstatusSinistroReponse, MeioPagamentoReponse


class SinistrosBase(BaseModel):
    valor: PositiveFloat
    data_pagamento: datetime


class SinistrosResponse(SinistrosBase):
    data_insercao: datetime
    data_atualizacao: datetime
    estatus_sinistro: EstatusSinistroReponse
    meio_pagamento: MeioPagamentoReponse
    apolice: ApoliceReponse

    model_config = ConfigDict(from_attributes=True)


class SinistrosSumaryResponse(SinistrosBase):
    data_insercao: datetime
    data_atualizacao: datetime
    estatus_sinistro: EstatusSinistroReponse
    meio_pagamento: MeioPagamentoReponse
    apolice_id: int

    model_config = ConfigDict(from_attributes=True)


class SinistrosCreate(SinistrosBase):
    pass


class SinistrosUpdate(BaseModel):
    pass
