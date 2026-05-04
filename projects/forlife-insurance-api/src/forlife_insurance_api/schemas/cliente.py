from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

from .dominios import CidadeResponse


class BRPhone(PhoneNumber):
    default_region_code = "BR"
    supported_regions = ["BR"]
    phone_format = "INTERNATIONAL"


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: BRPhone
    telefone: str
    endereco: str
    data_nascimento: date


class ClienteResponse(ClienteBase):
    cliente_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    cidade: CidadeResponse = Field(validation_alias="cidade")

    model_config = ConfigDict(from_attributes=True)


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    pass
