from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from forlife_insurance.core.config import get_database_settings

_engine: Engine | None = None
_session_local: sessionmaker[Session] | None = None


class Base(DeclarativeBase):
    pass


def get_engine() -> Engine:
    global _engine

    if _engine is None:
        settings = get_database_settings()
        _engine = create_engine(settings.url)

    return _engine


def init_database() -> None:
    Base.metadata.create_all(get_engine())


def get_session_local() -> sessionmaker[Session]:
    global _session_local

    if _session_local is None:
        _session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=get_engine(),
        )

    return _session_local


def get_db() -> Generator[Session, None, None]:
    session = get_session_local()()
    try:
        yield session
    finally:
        session.close()


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    session = get_session_local()()
    try:
        yield session
    finally:
        session.close()
