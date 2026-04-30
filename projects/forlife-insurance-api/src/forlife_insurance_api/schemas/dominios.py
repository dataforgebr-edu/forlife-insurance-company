from pydantic import BaseModel, ConfigDict


class DominiosBase(BaseModel):
    descricao: str


class ProdutoResponse(DominiosBase):
    produto_id: int

    model_config = ConfigDict(from_attributes=True)


class StatusApoliceResponse(DominiosBase):
    status_apolice_id: int

    model_config = ConfigDict(from_attributes=True)


class PeriodicidadePagamentoResponse(DominiosBase):
    periodicidade_id: int

    model_config = ConfigDict(from_attributes=True)


class MeioPagamentoResponse(DominiosBase):
    meio_pagamento_id: int

    model_config = ConfigDict(from_attributes=True)


class StatusSinistroResponse(DominiosBase):
    status_sinistro_id: int

    model_config = ConfigDict(from_attributes=True)


class EstadoBase(DominiosBase):
    uf: str


class EstadoResponse(EstadoBase):
    estado_id: int

    model_config = ConfigDict(from_attributes=True)


class CidadeResponse(DominiosBase):
    cidade_id: int
    estado: EstadoResponse

    model_config = ConfigDict(from_attributes=True)
