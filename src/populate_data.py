from __future__ import annotations

import argparse
import random
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from decimal import Decimal

from faker import Faker
from sqlalchemy import select
from sqlalchemy.orm import Session

from database.database import Base, Localsession, engine
from models.apolice import Apolice
from models.cliente import Cliente
from models.corretor import Corretor
from models.dominios import (
    Cidade,
    Estados,
    EstatusApolice,
    EstatusSinistro,
    MeioPagamento,
    PeriodicidadePagamento,
    Produtos,
)
from models.parcelas import Parcelas
from models.sinistros import Sinistros

faker = Faker("pt_BR")


@dataclass(frozen=True)
class ReferenceIds:
    estado_ids: list[int]
    cidades_ids: list[int]
    produto_ids: list[int]
    estatus_apolice_ids: list[int]
    periodicidade_ids: list[int]
    meio_pagamento_ids: list[int]
    estatus_sinistro_ids: list[int]


def money(min_value: float, max_value: float) -> Decimal:
    raw = Decimal(str(random.uniform(min_value, max_value)))
    return raw.quantize(Decimal("0.01"))


def add_months(base: datetime, months: int) -> datetime:
    month = base.month - 1 + months
    year = base.year + month // 12
    month = month % 12 + 1
    day = min(
        base.day,
        [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][
            month - 1
        ],
    )
    return base.replace(year=year, month=month, day=day)


def bootstrap_domain_data(session: Session) -> None:
    if not session.scalar(select(Estados.estado_id).limit(1)):
        session.add_all(
            [
                Estados(uf="SP", descricao="São Paulo"),
                Estados(uf="RJ", descricao="Rio de Janeiro"),
                Estados(uf="MG", descricao="Minas Gerais"),
                Estados(uf="PR", descricao="Paraná"),
                Estados(uf="RS", descricao="Rio Grande do Sul"),
                Estados(uf="BA", descricao="Bahia"),
            ]
        )
        session.flush()

    if not session.scalar(select(Cidade.cidade_id).limit(1)):
        cidades_por_uf = {
            "SP": ["São Paulo", "Campinas", "Santos", "Sorocaba"],
            "RJ": ["Rio de Janeiro", "Niterói", "Petrópolis", "Volta Redonda"],
            "MG": ["Belo Horizonte", "Uberlândia", "Contagem", "Juiz de Fora"],
            "PR": ["Curitiba", "Londrina", "Maringá", "Ponta Grossa"],
            "RS": ["Porto Alegre", "Caxias do Sul", "Pelotas", "Santa Maria"],
            "BA": ["Salvador", "Feira de Santana", "Vitória da Conquista", "Ilhéus"],
        }
        estado_ids_por_uf = {
            uf: estado_id
            for estado_id, uf in session.execute(
                select(Estados.estado_id, Estados.uf)
            ).all()
        }
        session.add_all(
            [
                Cidade(descricao=cidade, estado_id=estado_ids_por_uf[uf])
                for uf, cidades in cidades_por_uf.items()
                for cidade in cidades
                if uf in estado_ids_por_uf
            ]
        )

    if not session.scalar(select(Produtos.produto_id).limit(1)):
        session.add_all(
            [
                Produtos(descricao="Seguro de Vida"),
                Produtos(descricao="Seguro Auto"),
                Produtos(descricao="Seguro Residencial"),
            ]
        )

    if not session.scalar(select(EstatusApolice.estatus_apolice_id).limit(1)):
        session.add_all(
            [
                EstatusApolice(descricao="Ativa"),
                EstatusApolice(descricao="Cancelada"),
                EstatusApolice(descricao="Vencida"),
            ]
        )

    if not session.scalar(select(PeriodicidadePagamento.periodicidade_id).limit(1)):
        session.add_all(
            [
                PeriodicidadePagamento(descricao="Mensal"),
                PeriodicidadePagamento(descricao="Trimestral"),
                PeriodicidadePagamento(descricao="Semestral"),
                PeriodicidadePagamento(descricao="Anual"),
            ]
        )

    if not session.scalar(select(MeioPagamento.meio_pagamento_id).limit(1)):
        session.add_all(
            [
                MeioPagamento(descricao="Cartão de Crédito"),
                MeioPagamento(descricao="Boleto"),
                MeioPagamento(descricao="Débito em Conta"),
                MeioPagamento(descricao="Pix"),
            ]
        )

    if not session.scalar(select(EstatusSinistro.estatus_sinistro_id).limit(1)):
        session.add_all(
            [
                EstatusSinistro(descricao="Avisado"),
                EstatusSinistro(descricao="Em Analise"),
                EstatusSinistro(descricao="Pago"),
            ]
        )

    session.commit()


def load_reference_ids(session: Session) -> ReferenceIds:
    return ReferenceIds(
        estado_ids=session.scalars(select(Estados.estado_id)).all(),
        cidades_ids=session.scalars(select(Cidade.cidade_id)).all(),
        produto_ids=session.scalars(select(Produtos.produto_id)).all(),
        estatus_apolice_ids=session.scalars(
            select(EstatusApolice.estatus_apolice_id)
        ).all(),
        periodicidade_ids=session.scalars(
            select(PeriodicidadePagamento.periodicidade_id)
        ).all(),
        meio_pagamento_ids=session.scalars(
            select(MeioPagamento.meio_pagamento_id)
        ).all(),
        estatus_sinistro_ids=session.scalars(
            select(EstatusSinistro.estatus_sinistro_id)
        ).all(),
    )


def create_corretor(session: Session, estado_ids: list[int]) -> Corretor:
    data_insercao = faker.date_time_between(start_date="-6y", end_date="-60d")
    nome_faker = f"{faker.first_name()} {faker.last_name()}"
    email_faker = f"{nome_faker.replace(' ', '.').lower()}@{faker.free_email_domain()}"

    corretor = Corretor(
        nome=nome_faker,
        cnpj=faker.cnpj(),
        email=email_faker,
        estado_id=random.choice(estado_ids),
        data_insercao=data_insercao,
        data_atualizacao=data_insercao,
    )
    session.add(corretor)
    session.flush()
    return corretor


def create_cliente(session: Session, corretor: Corretor, refs: ReferenceIds) -> Cliente:
    inicio = corretor.data_insercao + timedelta(days=1)
    fim = inicio + timedelta(days=365)
    data_insercao = faker.date_time_between_dates(
        datetime_start=inicio, datetime_end=fim
    )
    nome_faker = f"{faker.first_name()} {faker.last_name()}"
    email_faker = f"{nome_faker.replace(' ', '.').lower()}@{faker.free_email_domain()}"

    cliente = Cliente(
        nome=nome_faker,
        email=email_faker,
        telefone=faker.msisdn()[:12],
        endereco=faker.street_address(),
        cidade_id=random.choice(refs.cidades_ids),
        data_nascimento=faker.date_of_birth(minimum_age=18, maximum_age=85),
        data_insercao=data_insercao,
        data_atualizacao=data_insercao,
    )
    session.add(cliente)
    session.flush()
    return cliente


def create_apolice(
    session: Session, cliente: Cliente, corretor: Corretor, refs: ReferenceIds
) -> Apolice:
    inicio_vigencia = cliente.data_insercao + timedelta(days=random.randint(1, 180))
    fim_vigencia = inicio_vigencia + timedelta(days=random.randint(365, 365 * 2))
    data_insercao = inicio_vigencia - timedelta(days=random.randint(1, 15))
    if data_insercao <= cliente.data_insercao:
        data_insercao = cliente.data_insercao + timedelta(days=1)

    apolice = Apolice(
        capital_segurado=money(50000, 500000),
        premio=money(120, 2500),
        inicio_vigencia=inicio_vigencia,
        fim_vigencia=fim_vigencia,
        status_apolice_id=random.choice(refs.estatus_apolice_ids),
        periodicidade_id=random.choice(refs.periodicidade_ids),
        produto_id=random.choice(refs.produto_ids),
        corretor_id=corretor.corretor_id,
        cliente_id=cliente.cliente_id,
        meio_pagamento_id=random.choice(refs.meio_pagamento_ids),
        data_insercao=data_insercao,
        data_atualizacao=data_insercao,
    )

    if cliente.data_insercao >= apolice.inicio_vigencia:
        raise ValueError(
            "Regra violada: cliente precisa ser cadastrado antes da apolice."
        )

    session.add(apolice)
    session.flush()
    return apolice


def create_parcelas(session: Session, apolice: Apolice, refs: ReferenceIds) -> int:
    periodicidade_meses = random.choice([1, 3, 6, 12])
    quantidade = max(
        1,
        min(
            12,
            int(
                (apolice.fim_vigencia - apolice.inicio_vigencia).days
                / (30 * periodicidade_meses)
            ),
        ),
    )

    parcelas = []
    for i in range(quantidade):
        data_periodo = add_months(apolice.inicio_vigencia, i * periodicidade_meses)
        data_emissao = max(apolice.data_insercao, data_periodo - timedelta(days=5))
        data_pagamento = data_periodo + timedelta(days=random.randint(0, 10))

        parcelas.append(
            Parcelas(
                valor=money(80, 1200),
                data_emissao=data_emissao,
                data_periodo=data_periodo,
                data_pagamento=data_pagamento,
                apolice_id=apolice.apolice_id,
                meio_pagamento_id=random.choice(refs.meio_pagamento_ids),
                data_insercao=data_emissao,
                data_atualizacao=data_emissao,
            )
        )

    session.add_all(parcelas)
    return len(parcelas)


def maybe_create_sinistro(
    session: Session, apolice: Apolice, refs: ReferenceIds, chance: float = 0.25
) -> bool:
    if random.random() > chance:
        return False

    inicio_pagamento = max(
        apolice.data_insercao + timedelta(days=1),
        apolice.inicio_vigencia + timedelta(days=5),
    )
    fim_pagamento = min(datetime.now(), apolice.fim_vigencia)
    if inicio_pagamento >= fim_pagamento:
        return False

    data_pagamento = faker.date_time_between_dates(
        datetime_start=inicio_pagamento, datetime_end=fim_pagamento
    )

    sinistro = Sinistros(
        valor=money(1000, 50000),
        data_pagamento=data_pagamento,
        estatus_sinistro_id=random.choice(refs.estatus_sinistro_ids),
        meio_pagamento_id=random.choice(refs.meio_pagamento_ids),
        apolice_id=apolice.apolice_id,
        data_insercao=data_pagamento,
        data_atualizacao=data_pagamento,
    )

    if apolice.data_insercao >= sinistro.data_pagamento:
        raise ValueError(
            "Regra violada: sinistro so pode ocorrer apos a apolice existir."
        )

    session.add(sinistro)
    return True


def run_batch(batch_size: int) -> tuple[int, int, int, int, int]:
    with Localsession() as session:
        bootstrap_domain_data(session)
        refs = load_reference_ids(session)

        corretores = 0
        clientes = 0
        apolices = 0
        parcelas = 0
        sinistros = 0

        for _ in range(batch_size):
            corretor = create_corretor(session, refs.estado_ids)
            cliente = create_cliente(session, corretor, refs)
            apolice = create_apolice(session, cliente, corretor, refs)
            parcelas += create_parcelas(session, apolice, refs)
            sinistros += int(maybe_create_sinistro(session, apolice, refs))

            corretores += 1
            clientes += 1
            apolices += 1

        session.commit()
        return corretores, clientes, apolices, parcelas, sinistros


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Populador continuo de dados para o dominio de seguros."
    )
    parser.add_argument("--mode", choices=["once", "continuous"], default="once")
    parser.add_argument("--batch-size", type=int, default=10)
    parser.add_argument("--interval-seconds", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    # Inicializar banco de dados
    Base.metadata.create_all(engine)

    args = parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        Faker.seed(args.seed)

    if args.mode == "once":
        co, c, a, p, s = run_batch(args.batch_size)
        print(
            "Batch concluido: "
            f"corretores={co}, clientes={c}, apolices={a}, parcelas={p}, sinistros={s}"
        )
        return

    try:
        while True:
            co, c, a, p, s = run_batch(args.batch_size)
            print(
                f"[{datetime.now().isoformat(timespec='seconds')}] "
                f"corretores={co} clientes={c} apolices={a} parcelas={p} sinistros={s}"
            )
            time.sleep(args.interval_seconds)
    except KeyboardInterrupt:
        print("Execucao encerrada pelo usuario.")


if __name__ == "__main__":
    main()
