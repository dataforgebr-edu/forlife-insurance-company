from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveFloat

from .apolice import ApoliceSumaryResponse
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
    apolice_id: int
    meio_pagamento: MeioPagamentoResponse

    model_config = ConfigDict(from_attributes=True)


class ParcelaCreate(ParcelaBase):
    apolice_id: int
    meio_pagamento_id: int


class ParcelaUpdate(BaseModel):
    valor: Optional[PositiveFloat] = None
    data_emissao: Optional[datetime] = None
    data_periodo: Optional[datetime] = None
    data_pagamento: Optional[datetime] = None
    meio_pagamento_id: Optional[int] = None
