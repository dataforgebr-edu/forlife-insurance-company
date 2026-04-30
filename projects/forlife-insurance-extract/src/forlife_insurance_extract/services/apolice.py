from collections.abc import Iterator
from datetime import datetime

from forlife_insurance_extract.repositories.apolice import (
    iter_apolices_extract,
    list_apolices_extract,
)
from forlife_insurance_extract.schemas.apolice import ApoliceExtractRow
from sqlalchemy.orm import Session


def get_apolices_extract(
    db: Session,
    *,
    changed_since: datetime | None = None,
    last_apolice_id: int | None = None,
    limit: int | None = None,
) -> list[ApoliceExtractRow]:
    """Serviço de extração em lote para apólices."""

    return list_apolices_extract(
        db,
        changed_since=changed_since,
        last_apolice_id=last_apolice_id,
        limit=limit,
    )


def stream_apolices_extract(
    db: Session,
    *,
    changed_since: datetime | None = None,
    last_apolice_id: int | None = None,
    limit: int | None = None,
) -> Iterator[ApoliceExtractRow]:
    """Serviço para pipelines que preferem consumo incremental."""

    return iter_apolices_extract(
        db,
        changed_since=changed_since,
        last_apolice_id=last_apolice_id,
        limit=limit,
    )
