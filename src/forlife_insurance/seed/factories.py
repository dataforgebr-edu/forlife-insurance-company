from __future__ import annotations

import random
from datetime import datetime, timedelta
from decimal import Decimal

from faker import Faker
from sqlalchemy.orm import Session

from forlife_insurance.models.apolice import Apolice
from forlife_insurance.models.cliente import Cliente
from forlife_insurance.models.corretor import Corretor
from forlife_insurance.models.parcelas import Parcela
from forlife_insurance.models.sinistros import Sinistro
from forlife_insurance.seed.bootstrap import PERIODICIDADE_MESES
from forlife_insurance.seed.types import CreatedApolice, DomainReferences

faker = Faker("pt_BR")


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


def random_name() -> str:
    return f"{faker.first_name()} {faker.last_name()}"


def random_email(name: str) -> str:
    normalized = name.replace(" ", ".").lower()
    return f"{normalized}@{faker.free_email_domain()}"


def create_corretor(session: Session, estado_ids: list[int]) -> Corretor:
    data_insercao = faker.date_time_between(start_date="-6y", end_date="-90d")
    nome = random_name()
    corretor = Corretor(
        nome=nome,
        cnpj=faker.cnpj(),
        email=random_email(nome),
        estado_id=random.choice(estado_ids),
        data_insercao=data_insercao,
        data_atualizacao=data_insercao,
    )
    session.add(corretor)
    session.flush()
    return corretor


def create_cliente(session: Session, cidade_ids: list[int]) -> Cliente:
    data_insercao = faker.date_time_between(start_date="-5y", end_date="-45d")
    nome = random_name()
    cliente = Cliente(
        nome=nome,
        email=random_email(nome),
        telefone=faker.msisdn()[:12],
        endereco=faker.street_address(),
        cidade_id=random.choice(cidade_ids),
        data_nascimento=faker.date_of_birth(minimum_age=18, maximum_age=85),
        data_insercao=data_insercao,
        data_atualizacao=data_insercao,
    )
    session.add(cliente)
    session.flush()
    return cliente


def create_apolice(
    session: Session,
    cliente: Cliente,
    corretor: Corretor,
    refs: DomainReferences,
) -> CreatedApolice:
    periodicidade_descricao = random.choice(list(refs.periodicidade_por_descricao))
    periodicidade_meses = PERIODICIDADE_MESES[periodicidade_descricao]

    inicio_base = max(cliente.data_insercao, corretor.data_insercao)
    inicio_vigencia = inicio_base + timedelta(days=random.randint(1, 120))
    fim_vigencia = inicio_vigencia + timedelta(days=random.randint(365, 730))

    apolice = Apolice(
        capital_segurado=money(50000, 500000),
        premio=money(120, 2500),
        inicio_vigencia=inicio_vigencia,
        fim_vigencia=fim_vigencia,
        data_insercao=inicio_vigencia,
        data_atualizacao=inicio_vigencia,
        status_apolice_id=random.choice(refs.status_apolice_ids),
        periodicidade_id=refs.periodicidade_por_descricao[periodicidade_descricao],
        produto_id=random.choice(refs.produto_ids),
        corretor_id=corretor.corretor_id,
        cliente_id=cliente.cliente_id,
        meio_pagamento_id=random.choice(refs.meio_pagamento_ids),
    )
    session.add(apolice)
    session.flush()
    return CreatedApolice(apolice=apolice, periodicidade_meses=periodicidade_meses)


def create_parcelas(
    session: Session,
    apolice: Apolice,
    periodicidade_meses: int,
    refs: DomainReferences,
) -> int:
    parcelas = []
    data_periodo = apolice.inicio_vigencia

    while data_periodo <= apolice.fim_vigencia:
        data_emissao = max(apolice.data_insercao, data_periodo - timedelta(days=5))
        data_pagamento = min(
            data_periodo + timedelta(days=random.randint(0, 10)),
            apolice.fim_vigencia,
        )
        parcelas.append(
            Parcela(
                valor=money(80, 1200),
                data_emissao=data_emissao,
                data_periodo=data_periodo,
                data_pagamento=data_pagamento,
                data_insercao=data_emissao,
                data_atualizacao=data_emissao,
                apolice_id=apolice.apolice_id,
                meio_pagamento_id=random.choice(refs.meio_pagamento_ids),
            )
        )
        data_periodo = add_months(data_periodo, periodicidade_meses)

    session.add_all(parcelas)
    session.flush()
    return len(parcelas)


def maybe_create_sinistro(
    session: Session,
    apolice: Apolice,
    refs: DomainReferences,
    chance: float = 0.25,
) -> bool:
    if random.random() > chance:
        return False

    inicio_pagamento = apolice.inicio_vigencia + timedelta(days=5)
    fim_pagamento = min(datetime.now(), apolice.fim_vigencia)
    if inicio_pagamento >= fim_pagamento:
        return False

    data_pagamento = faker.date_time_between_dates(
        datetime_start=inicio_pagamento,
        datetime_end=fim_pagamento,
    )

    sinistro = Sinistro(
        valor=money(1000, 50000),
        data_pagamento=data_pagamento,
        data_insercao=data_pagamento,
        data_atualizacao=data_pagamento,
        status_sinistro_id=random.choice(refs.status_sinistro_ids),
        meio_pagamento_id=random.choice(refs.meio_pagamento_ids),
        apolice_id=apolice.apolice_id,
    )
    session.add(sinistro)
    session.flush()
    return True
