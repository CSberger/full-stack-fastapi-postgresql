import secrets
from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


def required_if_uri_not_present(cls, v, values, field):
    if 'SQLALCHEMY_DATABASE_URI' not in values and v is None:
        raise ValueError(f'{field} or SQLALCHEMY_DATABASE_URI required')
    return v

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    PROJECT_NAME: str

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    POSTGRES_SERVER: Optional[str]
    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str]

    check_server = validator('POSTGRES_SERVER', allow_reuse=True)(required_if_uri_not_present)
    check_user = validator('POSTGRES_USER', allow_reuse=True)(required_if_uri_not_present)
    check_pw = validator('POSTGRES_PASSWORD', allow_reuse=True)(required_if_uri_not_present)
    check_db = validator('POSTGRES_DB', allow_reuse=True)(required_if_uri_not_present)

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    class Config:
        env_prefix = "{{ cookiecutter.env_prefix }}"
        case_sensitive = True


settings = Settings()
