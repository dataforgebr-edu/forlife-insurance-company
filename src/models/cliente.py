from datetime import date, datetime
from typing import Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    # se for necessário definir schemas diferentes para cada tabela
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
        ForeignKey("cidades.cidade_id"), nullable=False
    )
