import os

from dotenv import load_dotenv
from sqlalchemy import URL, MetaData, create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

# Configurações do banco PostgreSQL via variáveis de ambiente
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USER, DB_PASSWORD, DB_NAME]):
    raise ValueError(
        "Variáveis de ambiente DB_USER, DB_PASSWORD e DB_NAME são obrigatórias."
    )

url_object = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    database=DB_NAME,
)


# SQL_ALCHEMY_DATABASE = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
print(f"String de conexão com o banco= {url_object}")

engine = create_engine(url_object)

Localsession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Caso seja necessário definir um schema para todas as tabelas
# metadata_obj = MetaData(schema="seguros")


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
