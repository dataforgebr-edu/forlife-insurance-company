from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from forlife_insurance_core.database.database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from forlife_insurance_core.models.apolice import Apolice
    from forlife_insurance_core.models.dominios import MeioPagamento


class Parcela(Base):
    __tablename__ = "parcela"

    parcela_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    data_emissao: Mapped[datetime] = mapped_column(DateTime)
    data_periodo: Mapped[datetime] = mapped_column(DateTime)
    data_pagamento: Mapped[datetime] = mapped_column(DateTime)
    data_insercao: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    apolice_id: Mapped[int] = mapped_column(
        ForeignKey("apolice.apolice_id"), nullable=False
    )
    meio_pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("meio_pagamento.meio_pagamento_id"), nullable=False
    )

    apolice: Mapped[Apolice] = relationship(back_populates="parcelas")
    meio_pagamento: Mapped[MeioPagamento] = relationship(back_populates="parcelas")
