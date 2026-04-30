import os
from dataclasses import dataclass

from dotenv import load_dotenv
from sqlalchemy import URL


@dataclass(frozen=True)
class DatabaseSettings:
    user: str
    password: str
    host: str
    port: int
    name: str
    driver: str = "postgresql+psycopg2"

    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            database=self.name,
        )


def get_database_settings() -> DatabaseSettings:
    load_dotenv()

    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")

    if not db_user or not db_password or not db_name:
        raise ValueError(
            "As variáveis DB_USER, DB_PASSWORD e DB_NAME são obrigatórias."
        )

    return DatabaseSettings(
        user=db_user,
        password=db_password,
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        name=db_name,
    )
