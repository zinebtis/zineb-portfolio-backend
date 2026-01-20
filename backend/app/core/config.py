from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str = ""
    llm_github_token: str = ""
    model_name: str = "gpt-4o-mini"
    max_requests_per_minute: int = 30
    data_dir: str = "data"
    vectorstore_path: str = "data/vectorstore/index.faiss"
    chunks_path: str = "data/processed/chunks.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        protected_namespaces=("settings_",),
    )


class AppState(BaseModel):
    settings: Settings


settings = Settings()
