from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ApoliceBase(BaseModel):
    capital_segurado: float
    premio: float
    inicio_vigencia: datetime
    fim_vigencia: datetime


class ApoliceReponse(ApoliceBase):
    apolice_id: int
    data_insercao: datetime
    data_atualizacao: datetime

    model_config = ConfigDict(from_attributes=True)


class ApoliceCreate(ApoliceBase):
    pass


class ApoliceUpdate(BaseModel):
    pass
