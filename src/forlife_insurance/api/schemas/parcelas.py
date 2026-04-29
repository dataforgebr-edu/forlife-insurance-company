from datetime import datetime

from pydantic import BaseModel, ConfigDict, PositiveFloat

from .apolice import ApoliceReponse
from .dominios import MeioPagamentoReponse


class ParcelasBase(BaseModel):
    valor: PositiveFloat
    data_emissao: datetime
    data_periodo: datetime
    data_pagamento: datetime


class ParcelasResponse(ParcelasBase):
    parcela_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    apolice: ApoliceReponse
    meio_pagamento_parcela: MeioPagamentoReponse

    model_config = ConfigDict(from_attributes=True)


class ParcelasSumaryResponse(ParcelasBase):
    parcela_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    apolice_id: int
    meio_pagamento_parcela: MeioPagamentoReponse

    model_config = ConfigDict(from_attributes=True)


class ParcelasCreate(ParcelasBase):
    pass


class ParcelasUpdate(BaseModel):
    pass
