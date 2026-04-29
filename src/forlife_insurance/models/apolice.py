from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forlife_insurance.database.database import Base

if TYPE_CHECKING:
    from forlife_insurance.models.cliente import Cliente
    from forlife_insurance.models.corretor import Corretor
    from forlife_insurance.models.dominios import (
        EstatusApolice,
        MeioPagamento,
        PeriodicidadePagamento,
        Produtos,
    )
    from forlife_insurance.models.parcelas import Parcelas
    from forlife_insurance.models.sinistros import Sinistros


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

    estatus_apolice: Mapped[EstatusApolice] = relationship(back_populates="apolice")
    status_apolice_id: Mapped[int] = mapped_column(
        ForeignKey("estatus_apolice.estatus_apolice_id"), nullable=False
    )

    periodicidade_pagamento: Mapped[PeriodicidadePagamento] = relationship(
        back_populates="apolice"
    )
    periodicidade_id: Mapped[int] = mapped_column(
        ForeignKey("periodicidade_pagamento.periodicidade_id"), nullable=False
    )

    produtos: Mapped[Produtos] = relationship(back_populates="apolice")
    produto_id: Mapped[int] = mapped_column(
        ForeignKey("produtos.produto_id"), nullable=False
    )

    meio_pagamento: Mapped[MeioPagamento] = relationship(back_populates="apolice")
    meio_pagamento_id: Mapped[int] = mapped_column(
        ForeignKey("meio_pagamento.meio_pagamento_id"), nullable=False
    )

    corretor: Mapped[Corretor] = relationship(back_populates="apolice")
    corretor_id: Mapped[int] = mapped_column(
        ForeignKey("corretor.corretor_id"), nullable=False
    )

    cliente: Mapped[Cliente] = relationship(back_populates="apolice")
    cliente_id: Mapped[int] = mapped_column(
        ForeignKey("cliente.cliente_id"), nullable=False
    )

    sinistros: Mapped[Optional[Sinistros]] = relationship(back_populates="apolice")

    parcelas: Mapped[Parcelas] = relationship(back_populates="apolice")
