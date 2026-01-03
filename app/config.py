from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    
    supabase_url: str
    supabase_anon_key: str
    secret_key: str
    access_token_expire_minutes: int = 30
    algorithm: str
    docs_username: str
    docs_password: str

Settings = Settings()