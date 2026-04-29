from __future__ import annotations

from dataclasses import dataclass

from forlife_seed.models.apolice import Apolice


@dataclass(frozen=True)
class DomainReferences:
    estado_ids: list[int]
    cidade_ids: list[int]
    produto_ids: list[int]
    estatus_apolice_ids: list[int]
    periodicidade_por_descricao: dict[str, int]
    meio_pagamento_ids: list[int]
    estatus_sinistro_ids: list[int]


@dataclass(frozen=True)
class CreatedApolice:
    apolice: Apolice
    periodicidade_meses: int
