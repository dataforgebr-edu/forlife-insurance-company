from database.db import Base


class MyClass(Base):
    __tablename__ = "sometable"
    __table_args__ = {"schema": "some_schema"}
    # como declarar o schema diretamente na tabela explicitamente
