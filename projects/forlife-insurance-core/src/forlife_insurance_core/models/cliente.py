from __future__ import annotations

from datetime import date, datetime
from typing import TYPE_CHECKING, Optional

from forlife_insurance_core.database.database import Base
from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from forlife_insurance_core.models.apolice import Apolice
    from forlife_insurance_core.models.dominios import Cidade


class Cliente(Base):
    __tablename__ = "cliente"

    # Use schemas específicos por tabela quando a evolução do domínio exigir.
    # __table_args__ = {"schema": "seguros"}

    cliente_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50))
    telefone: Mapped[Optional[str]] = mapped_column(String(12))
    endereco: Mapped[Optional[str]] = mapped_column(String(200))
    data_nascimento: Mapped[date] = mapped_column(Date)
    data_insercao: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    cidade_id: Mapped[int] = mapped_column(
        ForeignKey("cidade.cidade_id"), nullable=False
    )
    cidades: Mapped[Cidade] = relationship(back_populates="cliente")
    apolices: Mapped[list[Apolice]] = relationship(back_populates="cliente")
