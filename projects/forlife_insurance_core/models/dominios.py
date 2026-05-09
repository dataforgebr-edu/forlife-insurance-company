from __future__ import annotations

from typing import TYPE_CHECKING

from forlife_insurance_core.database.database import Base
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from forlife_insurance_core.models.apolice import Apolice
    from forlife_insurance_core.models.cliente import Cliente
    from forlife_insurance_core.models.corretor import Corretor
    from forlife_insurance_core.models.parcelas import Parcela
    from forlife_insurance_core.models.sinistros import Sinistro


class Estado(Base):
    __tablename__ = "estado"

    estado_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uf: Mapped[str] = mapped_column(String(2))
    descricao: Mapped[str] = mapped_column(String(50))

    cidades: Mapped[list[Cidade]] = relationship(back_populates="estado")
    corretores: Mapped[list[Corretor]] = relationship(back_populates="estado")


class Cidade(Base):
    __tablename__ = "cidade"

    cidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    estado: Mapped[Estado] = relationship(back_populates="cidades")
    estado_id: Mapped[int] = mapped_column(
        ForeignKey("estado.estado_id"), nullable=False
    )
    cliente: Mapped[list[Cliente]] = relationship(back_populates="cidade")


class Produto(Base):
    __tablename__ = "produto"

    produto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolices: Mapped[list[Apolice]] = relationship(back_populates="produto")


class StatusApolice(Base):
    __tablename__ = "status_apolice"

    status_apolice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolices: Mapped[list[Apolice]] = relationship(back_populates="status_apolice")


class PeriodicidadePagamento(Base):
    __tablename__ = "periodicidade_pagamento"

    periodicidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolices: Mapped[list[Apolice]] = relationship(
        back_populates="periodicidade_pagamento"
    )


class MeioPagamento(Base):
    __tablename__ = "meio_pagamento"

    meio_pagamento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolices: Mapped[list[Apolice]] = relationship(back_populates="meio_pagamento")

    sinistros: Mapped[list[Sinistro]] = relationship(back_populates="meio_pagamento")

    parcelas: Mapped[list[Parcela]] = relationship(back_populates="meio_pagamento")


class StatusSinistro(Base):
    __tablename__ = "status_sinistro"

    status_sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    sinistros: Mapped[list[Sinistro]] = relationship(back_populates="status_sinistro")
