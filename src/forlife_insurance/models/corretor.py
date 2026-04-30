from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forlife_insurance.database.database import Base

if TYPE_CHECKING:
    from forlife_insurance.models.apolice import Apolice
    from forlife_insurance.models.dominios import Estado


class Corretor(Base):
    __tablename__ = "corretor"

    corretor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    cnpj: Mapped[str] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(50))
    data_insercao: Mapped[datetime] = mapped_column(DateTime)
    data_atualizacao: Mapped[datetime] = mapped_column(DateTime)

    estado_id: Mapped[int] = mapped_column(ForeignKey("estado.estado_id"))
    estado: Mapped[Estado] = relationship(back_populates="corretores")
    apolices: Mapped[list[Apolice]] = relationship(back_populates="corretor")
