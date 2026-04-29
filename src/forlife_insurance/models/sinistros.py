from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forlife_insurance.database.database import Base

if TYPE_CHECKING:
    from forlife_insurance.models.apolice import Apolice
    from forlife_insurance.models.dominios import EstatusSinistro, MeioPagamento


class Sinistros(Base):
    __tablename__ = "sinistros"

    sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    data_pagamento: Mapped[datetime] = mapped_column(DateTime)
    data_insercao: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    estatus_sinistro: Mapped[EstatusSinistro] = relationship(back_populates="sinistros")
    estatus_sinistro_id: Mapped[int] = mapped_column(
        ForeignKey("estatus_sinistro.estatus_sinistro_id"), nullable=False
    )

    meio_pagamento: Mapped[MeioPagamento] = relationship(back_populates="sinistros")
    meio_pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("meio_pagamento.meio_pagamento_id"), nullable=False
    )

    apolice: Mapped[Apolice] = relationship(back_populates="sinistros")
    apolice_id: Mapped[int] = mapped_column(
        ForeignKey("apolice.apolice_id"), nullable=False
    )
