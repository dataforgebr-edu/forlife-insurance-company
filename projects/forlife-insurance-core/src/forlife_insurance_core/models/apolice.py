from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from forlife_insurance_core.database.database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from forlife_insurance_core.models.cliente import Cliente
    from forlife_insurance_core.models.corretor import Corretor
    from forlife_insurance_core.models.dominios import (
        MeioPagamento,
        PeriodicidadePagamento,
        Produto,
        StatusApolice,
    )
    from forlife_insurance_core.models.parcelas import Parcela
    from forlife_insurance_core.models.sinistros import Sinistro


class Apolice(Base):
    __tablename__ = "apolice"

    apolice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    capital_segurado: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    premio: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    inicio_vigencia: Mapped[datetime] = mapped_column(DateTime)
    fim_vigencia: Mapped[datetime] = mapped_column(DateTime)
    data_insercao: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    status_apolice: Mapped[StatusApolice] = relationship(back_populates="apolices")
    status_apolice_id: Mapped[int] = mapped_column(
        ForeignKey("status_apolice.status_apolice_id"), nullable=False
    )

    periodicidade_pagamento: Mapped[PeriodicidadePagamento] = relationship(
        back_populates="apolices"
    )
    periodicidade_id: Mapped[int] = mapped_column(
        ForeignKey("periodicidade_pagamento.periodicidade_id"), nullable=False
    )

    produto: Mapped[Produto] = relationship(back_populates="apolices")
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produto.produto_id"), nullable=False
    )

    meio_pagamento: Mapped[MeioPagamento] = relationship(back_populates="apolices")
    meio_pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("meio_pagamento.meio_pagamento_id"), nullable=False
    )

    corretor: Mapped[Corretor] = relationship(back_populates="apolices")
    corretor_id: Mapped[int] = mapped_column(
        ForeignKey("corretor.corretor_id"), nullable=False
    )

    cliente: Mapped[Cliente] = relationship(back_populates="apolices")
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("cliente.cliente_id"), nullable=False
    )

    parcelas: Mapped[list[Parcela]] = relationship(back_populates="apolices")
    sinistros: Mapped[Sinistro] = relationship(back_populates="apolice")
