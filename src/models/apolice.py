from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Apolice(Base):
    __tablename__ = "apolice"
    __table_args__ = {"schema": "seguros"}

    apolice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    capital_segurado: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    premio: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    inicio_vigencia: Mapped[datetime] = mapped_column(DateTime)
    fim_vigencia: Mapped[datetime] = mapped_column(DateTime)
    data_insercao: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    status_apolice_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.estatus_apolice.estatus_apolice_id"), nullable=False
    )
    periodicidade_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.periodicidade_pagamento.periodicidade_id"), nullable=False
    )
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.produtos.produto_id"), nullable=False
    )
    corretor_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.corretor.corretor_id"), nullable=False
    )
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.cliente.cliente_id"), nullable=False
    )
    meio_pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.meio_pagamento.meio_pagamento_id"), nullable=False
    )
