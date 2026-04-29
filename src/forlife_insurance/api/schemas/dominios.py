from pydantic import BaseModel, ConfigDict


class DominiosBase(BaseModel):
    descricao: str


class ProdutoReponse(DominiosBase):
    produto_id: int

    model_config = ConfigDict(from_attributes=True)


class EstatusApoliceReponse(DominiosBase):
    estatus_apolice_id: int

    model_config = ConfigDict(from_attributes=True)


class PeriodicidadePagamentoReponse(DominiosBase):
    periodicidade_id: int

    model_config = ConfigDict(from_attributes=True)


class MeioPagamentoReponse(DominiosBase):
    meio_pagamento_id: int

    model_config = ConfigDict(from_attributes=True)


class EstatusSinistroReponse(DominiosBase):
    estatus_sinistro_id: int

    model_config = ConfigDict(from_attributes=True)


class EstadosBase(DominiosBase):
    uf: str


class EstadosReponse(EstadosBase):
    estado_id: int

    model_config = ConfigDict(from_attributes=True)


class CidadesReponse(DominiosBase):
    cidade_id: int
    estados: EstadosReponse

    model_config = ConfigDict(from_attributes=True)
