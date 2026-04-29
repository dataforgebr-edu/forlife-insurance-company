from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from forlife_insurance.database.database import Base

if TYPE_CHECKING:
    from forlife_insurance.models.apolice import Apolice
    from forlife_insurance.models.parcelas import Parcelas
    from forlife_insurance.models.sinistros import Sinistros


class Estados(Base):
    __tablename__ = "estados"

    estado_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    uf: Mapped[str] = mapped_column(String(2))
    descricao: Mapped[str] = mapped_column(String(50))

    cidades: Mapped[list[Cidade]] = relationship(back_populates="estados")


class Cidade(Base):
    __tablename__ = "cidades"

    cidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    estados: Mapped[Estados] = relationship(back_populates="cidades")
    estado_id: Mapped[int] = mapped_column(
        ForeignKey("estados.estado_id"), nullable=False
    )


class Produtos(Base):
    __tablename__ = "produtos"

    produto_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolice: Mapped[list[Apolice]] = relationship(back_populates="produtos")


class EstatusApolice(Base):
    __tablename__ = "estatus_apolice"

    estatus_apolice_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolice: Mapped[list[Apolice]] = relationship(back_populates="estatus_apolice")


class PeriodicidadePagamento(Base):
    __tablename__ = "periodicidade_pagamento"

    periodicidade_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolice: Mapped[list[Apolice]] = relationship(
        back_populates="periodicidade_pagamento"
    )

    sinistro: Mapped[list[Sinistros]] = relationship(
        back_populates="periodicidade_pagamento"
    )


class MeioPagamento(Base):
    __tablename__ = "meio_pagamento"

    meio_pagamento_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))

    apolice: Mapped[list[Apolice]] = relationship(back_populates="meio_pagamento")

    sinistro: Mapped[list[Sinistros]] = relationship(back_populates="meio_pagamento")

    parcela: Mapped[list[Parcelas]] = relationship(back_populates="meio_pagamento")


class EstatusSinistro(Base):
    __tablename__ = "estatus_sinistro"

    estatus_sinistro_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    descricao: Mapped[str] = mapped_column(String(100))
