from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Estados(Base):
    __tablename__ = "estados"
    __table_args__ = {"schema": "seguros"}

    estado_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uf: Mapped[str] = mapped_column(String(2))
    descricao: Mapped[str] = mapped_column(String(50))

    cliente_back: Mapped[List["Cliente"]] = relationship(back_populates="estado_back")
    corretor_back: Mapped[List["Corretor"]] = relationship(
        back_populates="corretor_back"
    )


class Produtos(Base):
    __tablename__ = "produtos"
    __table_args__ = {"schema", "seguros"}

    produto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class EstatusApolice(Base):
    __tablename__ = "estatus_apolice"
    __table_args__ = {"schema", "seguros"}

    status_apolice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class PeriodicidadePagamento(Base):
    __tablename__ = "periodicidade_pagamento"
    __table_args__ = {"schema", "seguros"}

    periodicidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class MeioPagamento(Base):
    __tablename__ = "meio_pagamento"
    __table_args__ = {"schema", "seguros"}

    meio_pagamento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class EstatusSinistro(Base):
    __tablename__ = "estatus_sinistro"
    __table_args__ = {"schema", "seguros"}

    estatus_sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))
