import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env', env_file_encoding='utf-8', case_sensitive=True
    )

    TEST_MODE: int

    # POSTGRES DATABASE
    POSTGRES_PASSWORD: str
    POSTGRES_DATABASE: str

    # REDIS DATABASE

    @property
    def pg_dns(self):
        url = 'postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{name}'.format(
            user=os.environ['POSTGRES_USER'],
            pwd=self.POSTGRES_PASSWORD,
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            name=self.POSTGRES_DATABASE,
        )
        return url if not self.TEST_MODE else url + '_test'

    @property
    def redis_dns(self):
        url = 'redis://{host}:6379'.format(
            host=os.environ['REDIS_HOST'],
        )
        return url if not self.TEST_MODE else url + '/1'

    @property
    def base_url(self):
        return '/api/v1' if not self.TEST_MODE else '/test-api/v1'


settings = Settings()
