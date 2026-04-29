from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from forlife_insurance.database.database import Base


class Estados(Base):
    __tablename__ = "estados"

    estado_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uf: Mapped[str] = mapped_column(String(2))
    descricao: Mapped[str] = mapped_column(String(50))


class Cidade(Base):
    __tablename__ = "cidades"

    cidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))
    estado_id: Mapped[int] = mapped_column(
        ForeignKey("estados.estado_id"), nullable=False
    )


class Produtos(Base):
    __tablename__ = "produtos"

    produto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class EstatusApolice(Base):
    __tablename__ = "estatus_apolice"

    estatus_apolice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class PeriodicidadePagamento(Base):
    __tablename__ = "periodicidade_pagamento"

    periodicidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class MeioPagamento(Base):
    __tablename__ = "meio_pagamento"

    meio_pagamento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))


class EstatusSinistro(Base):
    __tablename__ = "estatus_sinistro"

    estatus_sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))
