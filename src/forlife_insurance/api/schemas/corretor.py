from datetime import datetime

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
    pass


class CorretorUpdate(BaseModel):
    pass
