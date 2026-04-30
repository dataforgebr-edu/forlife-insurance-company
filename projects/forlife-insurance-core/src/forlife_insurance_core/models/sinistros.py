from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from forlife_insurance_core.database.database import Base
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from forlife_insurance_core.models.apolice import Apolice
    from forlife_insurance_core.models.dominios import MeioPagamento, StatusSinistro


class Sinistro(Base):
    __tablename__ = "sinistro"

    sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    data_pagamento: Mapped[datetime] = mapped_column(DateTime)
    data_insercao: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    status_sinistro: Mapped[StatusSinistro] = relationship(back_populates="sinistros")
    status_sinistro_id: Mapped[int] = mapped_column(
        ForeignKey("status_sinistro.status_sinistro_id"), nullable=False
    )

    meio_pagamento: Mapped[MeioPagamento] = relationship(back_populates="sinistros")
    meio_pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("meio_pagamento.meio_pagamento_id"), nullable=False
    )

    apolice: Mapped[Apolice] = relationship(back_populates="sinistros")
    apolice_id: Mapped[int] = mapped_column(
        ForeignKey("apolice.apolice_id"), nullable=False
    )
