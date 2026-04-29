from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Cliente(Base):
    __tablename__ = "cliente"
    __table_args__ = {"schema": "seguros"}

    cliente_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    telefone: Mapped[Optional[str]] = mapped_column(String(12))
    endereco: Mapped[Optional[str]] = mapped_column(String(200))
    cidade: Mapped[Optional[str]] = mapped_column(String(50))
    data_nascimento: Mapped[date] = mapped_column(Date)
    data_insercao: Mapped[datetime] = mapped_column(DateTime)
    data_atualizacao: Mapped[datetime] = mapped_column(DateTime)

    estado_id: Mapped[int] = mapped_column(
        ForeignKey("seguros.estados.estado_id"), nullable=False
    )
    estado_back: Mapped["Estados"] = relationship(back_populates="cliente_back")
