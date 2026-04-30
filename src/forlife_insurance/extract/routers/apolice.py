from __future__ import annotations

import json
from datetime import datetime

from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from forlife_insurance.database.database import get_db
from forlife_insurance.extract.schemas.apolice import ApoliceExtractRow
from forlife_insurance.extract.services.apolice import (
    get_apolices_extract,
    stream_apolices_extract,
)

router = APIRouter()
# prefix="/apolices", tags=["extract-apolices"]


@router.get("/apolices", response_model=list[ApoliceExtractRow])
def list_apolices_extract_endpoint(
    changed_since: datetime | None = Query(default=None),
    last_apolice_id: int | None = Query(default=None, ge=1),
    limit: int = Query(default=5000, ge=1, le=50000),
    db: Session = Depends(get_db),
) -> list[ApoliceExtractRow]:
    return get_apolices_extract(
        db,
        changed_since=changed_since,
        last_apolice_id=last_apolice_id,
        limit=limit,
    )


@router.get("/stream")
def stream_apolices_extract_endpoint(
    changed_since: datetime | None = Query(default=None),
    last_apolice_id: int | None = Query(default=None, ge=1),
    limit: int = Query(default=5000, ge=1, le=50000),
    db: Session = Depends(get_db),
) -> StreamingResponse:
    def generate() -> bytes:
        for row in stream_apolices_extract(
            db,
            changed_since=changed_since,
            last_apolice_id=last_apolice_id,
            limit=limit,
        ):
            yield json.dumps(row.model_dump(mode="json"), ensure_ascii=False).encode(
                "utf-8"
            )
            yield b"\n"

    return StreamingResponse(generate(), media_type="application/x-ndjson")
