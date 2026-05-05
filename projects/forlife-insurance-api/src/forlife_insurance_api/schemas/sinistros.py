from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, PositiveFloat

from .dominios import MeioPagamentoResponse, StatusSinistroResponse


class SinistroBase(BaseModel):
    valor: PositiveFloat
    data_pagamento: datetime


class SinistroResponse(SinistroBase):
    sinistro_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    apolice_id: int
    status_sinistro: StatusSinistroResponse
    meio_pagamento: MeioPagamentoResponse

    model_config = ConfigDict(from_attributes=True)


class SinistroCreate(SinistroBase):
    apolice_id: int
    status_sinistro_id: int
    meio_pagamento_id: int


class SinistroUpdate(BaseModel):
    valor: Optional[PositiveFloat] = None
    data_pagamento: Optional[datetime] = None
    status_sinistro_id: Optional[int] = None
    meio_pagamento_id: Optional[int] = None
