from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Sinistros(Base):
    __tablename__ = "sinistros"
    __table_args__ = {"schema": "seguros"}

    sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    valor: Mapped[float] = mapped_column(Numeric(precision=10, scale=2))
    data_pagamento: Mapped[datetime] = mapped_column(datetime)
    data_insercao: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    estatus_sinistro_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.estatus_sinistro.estatus_sinistro_id"), nullable=False
    )
    meio_pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.meio_pagamento.meio_pagamento_id"), nullable=False
    )
    apolice_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.apolice.apolice_id"), nullable=False
    )
