from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Corretor(Base):
    __tablename__ = "corretor"
    __table_args__ = {"schema": "seguros"}

    corretor_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    cnpj: Mapped[str] = mapped_column(String(100))
    email: Mapped[Optional[str]] = mapped_column(String(12))
    data_insercao: Mapped[datetime] = mapped_column(DateTime)
    data_atualizacao: Mapped[datetime] = mapped_column(DateTime)

    estado_id: Mapped[int] = mapped_column(ForeignKey("seguros.estados.estado_id"))
    estado_back: Mapped["Estados"] = relationship(back_populates="corretor_back")
