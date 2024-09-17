from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Annotated
from pydantic import BeforeValidator


def parse_cors_origins(variable: str) -> list[str]:
    if isinstance(variable, str):
        return [item.strip() for item in variable.split(",")]
    
    raise ValueError(variable)


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    echo_sql: bool
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    cors_origins: Annotated[str | list, BeforeValidator(parse_cors_origins)] = []

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
