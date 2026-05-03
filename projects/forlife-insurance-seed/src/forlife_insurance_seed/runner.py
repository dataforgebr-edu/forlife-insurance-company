from __future__ import annotations

import argparse
import random
import time
from datetime import datetime

from faker import Faker
from forlife_insurance_core.database.database import init_database, session_scope
from forlife_insurance_core.models.cliente import Cliente
from forlife_insurance_core.models.corretor import Corretor
from forlife_insurance_seed.bootstrap import (
    bootstrap_domain_data,
    load_domain_references,
)
from forlife_insurance_seed.factories import (
    create_apolice,
    create_cliente,
    create_corretor,
    create_parcelas,
    maybe_create_sinistro,
)
from sqlalchemy import select
from sqlalchemy.orm import Session


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Seed de dados para o domínio de seguros."
    )
    parser.add_argument("--mode", choices=["once", "continuous"], default="once")
    parser.add_argument("--batch-size", type=int, default=5)
    parser.add_argument("--interval-seconds", type=int, default=20)
    parser.add_argument("--seed", type=int, default=None)
    return parser.parse_args()


def _seed_random_generators(seed: int | None) -> None:
    if seed is None:
        return
    random.seed(seed)
    Faker.seed(seed)


def _ensure_minimum_pool(
    session: Session,
    refs,
    batch_size: int,
) -> tuple[list[Corretor], list[Cliente]]:
    corretores = session.scalars(select(Corretor)).all()
    clientes = session.scalars(select(Cliente)).all()

    minimum_entities = max(1, batch_size // 4)

    while len(corretores) < minimum_entities:
        corretores.append(create_corretor(session, refs.estado_ids))

    while len(clientes) < minimum_entities:
        clientes.append(create_cliente(session, refs.cidade_ids))

    return corretores, clientes


def run_batch(
    batch_size: int, bootstrap_domain: bool
) -> tuple[int, int, int, int, int]:
    with session_scope() as session:
        if bootstrap_domain:
            bootstrap_domain_data(session)

        refs = load_domain_references(session)
        corretores, clientes = _ensure_minimum_pool(session, refs, batch_size)

        corrs = 0
        clis = 0
        apols = 0
        parcs = 0
        sins = 0

        for _ in range(batch_size):
            corretor = random.choice(corretores)
            cliente = random.choice(clientes)
            apolice_context = create_apolice(session, cliente, corretor, refs)
            parcs += create_parcelas(
                session,
                apolice_context.apolice,
                apolice_context.periodicidade_meses,
                refs,
            )
            sins += int(maybe_create_sinistro(session, apolice_context.apolice, refs))
            apols += 1

            if random.random() < 0.35:
                corretores.append(create_corretor(session, refs.estado_ids))
                corrs += 1

            if random.random() < 0.45:
                clientes.append(create_cliente(session, refs.cidade_ids))
                clis += 1

        session.commit()
        return corrs, clis, apols, parcs, sins


def main() -> None:
    init_database()
    args = parse_args()
    _seed_random_generators(args.seed)

    if args.mode == "once":
        corrs, clis, apols, parcs, sins = run_batch(
            args.batch_size, bootstrap_domain=True
        )
        print(
            "Batch concluido: "
            f"corretores={corrs}, clientes={clis}, apólices={apols}, parcelas={parcs}, sinistros={sins}"
        )
        return

    bootstrap_done = False
    try:
        while True:
            corrs, clis, apols, parcs, sins = run_batch(
                args.batch_size,
                bootstrap_domain=not bootstrap_done,
            )
            bootstrap_done = True
            print(
                f"[{datetime.now().isoformat(timespec='seconds')}] "
                f"corretores={corrs} clientes={clis} apólices={apols} parcelas={parcs} sinistros={sins}"
            )
            time.sleep(args.interval_seconds)
    except KeyboardInterrupt:
        print("Execução encerrada pelo usuário.")


if __name__ == "__main__":
    main()
