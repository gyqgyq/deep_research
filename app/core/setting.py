from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    async_database_url: str
    dashscope_api_key: str

settings = Settings()

if __name__ == "__main__":
    print(settings.async_database_url)
    print(settings.dashscope_api_key)