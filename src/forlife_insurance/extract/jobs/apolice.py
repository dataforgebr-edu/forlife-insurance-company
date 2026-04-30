from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from forlife_insurance.database.database import init_database, session_scope
from forlife_insurance.extract.services.apolice import stream_apolices_extract


@dataclass(frozen=True)
class ApoliceExtractJobConfig:
    output_path: Path
    changed_since: datetime | None = None
    last_apolice_id: int | None = None
    limit: int | None = None


@dataclass(frozen=True)
class ApoliceExtractJobResult:
    output_path: Path
    rows_written: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Job de extração de apolices para NDJSON."
    )
    parser.add_argument("--output-path", required=True)
    parser.add_argument("--changed-since", default=None)
    parser.add_argument("--last-apolice-id", type=int, default=None)
    parser.add_argument("--limit", type=int, default=None)
    return parser.parse_args()


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value)


def run_apolice_extract_job(
    config: ApoliceExtractJobConfig,
) -> ApoliceExtractJobResult:
    config.output_path.parent.mkdir(parents=True, exist_ok=True)

    rows_written = 0
    with session_scope() as db:
        with config.output_path.open("w", encoding="utf-8") as file:
            for row in stream_apolices_extract(
                db,
                changed_since=config.changed_since,
                last_apolice_id=config.last_apolice_id,
                limit=config.limit,
            ):
                file.write(json.dumps(row.model_dump(mode="json"), ensure_ascii=False))
                file.write("\n")
                rows_written += 1

    return ApoliceExtractJobResult(
        output_path=config.output_path,
        rows_written=rows_written,
    )


def main() -> None:
    init_database()
    args = parse_args()
    result = run_apolice_extract_job(
        ApoliceExtractJobConfig(
            output_path=Path(args.output_path),
            changed_since=_parse_datetime(args.changed_since),
            last_apolice_id=args.last_apolice_id,
            limit=args.limit,
        )
    )
    print(
        f"Job concluido: rows_written={result.rows_written}, output_path={result.output_path}"
    )


if __name__ == "__main__":
    main()
