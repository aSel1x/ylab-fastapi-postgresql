from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', case_sensitive=True
    )

    TEST_MODE: int

    # POSTGRES DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    # REDIS DATABASE
    REDIS_HOST: str
    REDIS_PASSWORD: str

    @property
    def pg_dns(self):
        url = f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}'
        return url if not self.TEST_MODE else url + '_test'

    @property
    def redis_dns(self):
        url = f'redis://:119733@91.201.54.16'
        return url if not self.TEST_MODE else url + '/1'

    @property
    def base_url(self):
        return '/api/v1' if not self.TEST_MODE else '/test-api/v1'


settings = Settings()
