from typing import Annotated

from pydantic import BeforeValidator, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


def parse_cors_origins(variable: str) -> list[str]:
    if isinstance(variable, str):
        return [item.strip() for item in variable.split(",")]

    raise ValueError(variable)


class Settings(BaseSettings):
    # app settings
    app_name: str = "FastAPI project"
    app_description: str | None = None
    app_version: str | None = None
    contact_name: str | None = None
    contact_email: str | None = None
    contact_url: str | None = None

    # first admin settings
    admin_email: str
    admin_password: str

    # main postgres db settings
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    echo_sql: bool

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )

    # test postgres db settings
    test_db_user: str
    test_db_password: str
    test_db_host: str
    test_db_port: int
    test_db_name: str

    @computed_field
    @property
    def test_postgres_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql",
            username=self.test_db_user,
            password=self.test_db_password,
            host=self.test_db_host,
            port=self.test_db_port,
            path=self.test_db_name,
        )

    # crypt settings
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # cors settings
    cors_origins: Annotated[str | list, BeforeValidator(parse_cors_origins)] = []

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
