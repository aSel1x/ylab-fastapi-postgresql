import redis.asyncio
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=('.env', '.env.developer'), env_file_encoding='utf-8', case_sensitive=True
    )

    TEST_MODE: bool
    DEVELOPER: bool | None = False

    # POSTGRES DATABASE
    POSTGRES_HOST: str
    POSTGRES_PORT: int | None = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str

    # REDIS DATABASE
    REDIS_HOST: str
    REDIS_PASSWORD: str | None

    # RABBIT BROKER
    RABBIT_HOST: str | None = None
    RABBITMQ_DEFAULT_USER: str | None
    RABBITMQ_DEFAULT_PASS: str | None

    @property
    def pg_dns(self):
        url = 'postgresql+asyncpg://{user}:{pwd}@{host}:{port}/{name}'.format(
            user=self.POSTGRES_USER,
            pwd=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            name=self.POSTGRES_DB,
        )
        return url

    @property
    def sync_pg_dns(self):
        url = 'postgresql://{user}:{pwd}@{host}:{port}/{name}'.format(
            user=self.POSTGRES_USER,
            pwd=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            name=self.POSTGRES_DB,
        )
        return url

    @property
    def aioredis(self) -> redis.asyncio.Redis:
        url = 'redis://:{pwd}@{host}:6379'.format(
            pwd=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
        )
        return redis.asyncio.from_url(url + '/0' if not self.TEST_MODE else url + '/1')

    @property
    def redis(self) -> redis.Redis:
        url = 'redis://:{pwd}@{host}:6379'.format(
            pwd=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
        )
        return redis.from_url(url + '/0' if not self.TEST_MODE else url + '/1')

    @property
    def redis_dns(self) -> str:
        url = 'redis://:{pwd}@{host}:6379'.format(
            pwd=self.REDIS_PASSWORD,
            host=self.REDIS_HOST,
        )
        return url + '/0' if not self.TEST_MODE else url + '/1'

    @property
    def rabbit_dns(self):
        url = 'amqp://{user}:{pwd}@{host}:5672//'.format(
            host=self.RABBIT_HOST,
            user=self.RABBITMQ_DEFAULT_USER,
            pwd=self.RABBITMQ_DEFAULT_PASS,
        )
        return url

    @property
    def base_url(self):
        return '/api/v1' if not self.TEST_MODE else '/test-api/v1'


settings = Settings()
