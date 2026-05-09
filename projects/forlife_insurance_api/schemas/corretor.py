from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr
from pydantic_br import CNPJMask

from .dominios import EstadoResponse


class CorretorBase(BaseModel):
    nome: str
    cnpj: CNPJMask
    email: EmailStr


class CorretorResponse(CorretorBase):
    corretor_id: int
    data_insercao: datetime
    data_atualizacao: datetime
    estado: EstadoResponse

    model_config = ConfigDict(from_attributes=True)


class CorretorCreate(CorretorBase):
    estado_id: int


class CorretorUpdate(BaseModel):
    nome: Optional[str] = None
    cnpj: Optional[CNPJMask] = None
    email: Optional[EmailStr] = None
    estado_id: Optional[int] = None
