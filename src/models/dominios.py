from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base


class Estados(Base):
    __tablename__ = "estados"
    __table_args__ = {"schema": "seguros"}

    estado_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uf: Mapped[str] = mapped_column(String(2))
    descricao: Mapped[str] = mapped_column(String(50))


class Produtos(Base):
    __tablename__ = "produtos"
    __table_args__ = {"schema": "seguros"}

    produto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class EstatusApolice(Base):
    __tablename__ = "estatus_apolice"
    __table_args__ = {"schema": "seguros"}

    estatus_apolice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class PeriodicidadePagamento(Base):
    __tablename__ = "periodicidade_pagamento"
    __table_args__ = {"schema": "seguros"}

    periodicidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class MeioPagamento(Base):
    __tablename__ = "meio_pagamento"
    __table_args__ = {"schema": "seguros"}

    meio_pagamento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class EstatusSinistro(Base):
    __tablename__ = "estatus_sinistro"
    __table_args__ = {"schema": "seguros"}

    estatus_sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))
