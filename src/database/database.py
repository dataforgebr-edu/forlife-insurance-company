from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

BASE_DIR = Path(__file__).resolve().parent

SQL_ALCHEMY_DATABASE = f"sqlite:///{BASE_DIR / 'emissao.db'}"

engine = create_engine(SQL_ALCHEMY_DATABASE)

Localsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = Localsession()
    try:
        yield db
    finally:
        db.close()


"""
# como declarar o mesmo schema para todas as tabelas do banco

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

metadata_obj = MetaData(schema="some_schema")


class Base(DeclarativeBase):
    metadata = metadata_obj


class MyClass(Base):
    # will use "some_schema" by default
    __tablename__ = "sometable"
"""
