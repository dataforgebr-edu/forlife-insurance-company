import re
from datetime import date, datetime
from typing import Annotated, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.functional_validators import AfterValidator
from pydantic_extra_types.phone_numbers import PhoneNumber

from .dominios import CidadeResponse


class BRPhone(PhoneNumber):
    default_region_code = "BR"
    supported_regions = ["BR"]
    phone_format = "INTERNATIONAL"


def _sanitizar_telefone(v: str) -> str:
    valor = re.sub(r"[\s+\-]", "", v)
    return valor


TelefoneBR = Annotated[BRPhone, AfterValidator(_sanitizar_telefone)]


class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    telefone: TelefoneBR
    endereco: str
    data_nascimento: date


class ClienteResponse(ClienteBase):
    cliente_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    cidade: CidadeResponse = Field(validation_alias="cidade")

    model_config = ConfigDict(from_attributes=True)


class ClienteCreate(ClienteBase):
    cidade_id: int


class ClienteUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    telefone: Optional[TelefoneBR] = None
    endereco: Optional[str] = None
    data_nascimento: Optional[date] = None
    cidade_id: Optional[int] = None
