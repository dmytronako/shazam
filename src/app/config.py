import os
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=env_path)
    db_url: str


settings = Settings()
