from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from forlife_insurance.core.config import get_database_settings

_engine: Engine | None = None
_session_local: sessionmaker | None = None


class Base(DeclarativeBase):
    pass


def get_engine() -> Engine:
    global _engine

    if _engine is None:
        settings = get_database_settings()
        _engine = create_engine(settings.url)

    return _engine


def get_session_local() -> sessionmaker:
    global _session_local

    if _session_local is None:
        _session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )

    return _session_local


def get_db():
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()
