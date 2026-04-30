from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, PositiveInt


class ApoliceExtractQuery(BaseModel):
    """Parâmetros para extração incremental de apólices."""

    changed_since: datetime | None = None
    last_apolice_id: int | None = None
    limit: PositiveInt = 5000


class ApoliceExtractRow(BaseModel):
    """Linha plana para ingestão em data lake."""

    apolice_id: int
    capital_segurado: Decimal
    premio: Decimal
    inicio_vigencia: datetime
    fim_vigencia: datetime
    data_insercao: datetime
    data_atualizacao: datetime
    status_apolice_id: int
    status_apolice_descricao: str
    periodicidade_id: int
    periodicidade_descricao: str
    produto_id: int
    produto_descricao: str
    meio_pagamento_id: int
    meio_pagamento_descricao: str
    corretor_id: int
    corretor_nome: str
    corretor_cnpj: str
    corretor_email: str | None
    cliente_id: int
    cliente_nome: str
    cliente_email: str
    cliente_telefone: str | None
    cliente_endereco: str | None
    cliente_data_nascimento: date
    cidade_id: int
    cidade_descricao: str
    estado_id: int
    estado_uf: str
    estado_descricao: str

    model_config = ConfigDict(from_attributes=True)
