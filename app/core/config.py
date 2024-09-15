from enum import Enum

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class LogLevel(str, Enum):
    DEBUG = 'debug'
    INFO = 'info'
    WARNING = 'warning'
    ERROR = 'error'
    CRITICAL = 'critical'
    
    
class Settings(BaseSettings):
    """Настройки проекта"""

    project_name: str = Field(title='Название проекта')
    api_v1_prefix: str = Field(title='Префикс первой версии API', default='/api/v1')
    http_protocol: str = Field(default='http')
    port: str | int = Field(default='8000')
    domain_host_name: str = Field(default='127.0.0.1')
    log_level: LogLevel = Field(title='Уровень логирования', default=LogLevel.INFO)  
    telegram_client_password: str = Field(
        title='Пароль для авторизации клиентов из телеграмма'
    )  
    
    # region Настройки бота
    bot_token: str = Field(title='Токен бота')
    message_per_second: float = Field(title='Кол-во сообщений в секунду', default=1)  

    # region Настройки JWT
    secret_key: str = Field(title='Секретный ключ')
    algorithm: str = Field(title='JWT Алгоритм', default='HS256')
    access_expire_minutes: int = Field(
        title='Срок жизни access токена в минутах',
        default=20
    )
    refresh_expire_days: int = Field(
        title='Срок жизни refresh токена в днях',
        default=30
    )
    # endregion

    # region Настройки БД
    db_user: str = Field(title='Пользователь БД')
    db_password: str = Field(title='Пароль БД')
    db_host: str = Field(title='Хост БД')
    db_port: int = Field(title='Порт ДБ', default='5432')
    db_name: str = Field(title='Название БД')
    metadata_naming_convention: dict[str, str] = Field(
        default={
            'ix': 'ix_%(column_0_label)s',
            'uq': 'uq_%(table_name)s_%(column_0_N_name)s',
            'ck': 'ck_%(table_name)s_%(constraint_name)s',
            'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
            'pk': 'pk_%(table_name)s'
        })

    sqlite_default_url: str = Field(
        default='sqlite+aiosqlite:///./db.sqlite3'
    )

    # endregion

    container_wiring_modules: list = Field(
        title='Модули контейнера',
        default=[
            'app.api.v1.deps',
            'app.api.v1.endpoints.user',
            'app.api.v1.endpoints.auth',
            'app.api.v1.endpoints.note',
            'app.bot.handlers.note',
            
        ]
    )

    @property
    def db_url(self) -> str:
        return self.sqlite_default_url
    
    @property
    def postgres_url(self) -> str:
        if self.db_url:
            return self.db_url
        return str(PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=f"{self.db_name}",
        ))
    
    @property
    def web_url(self) -> str:
        return f'{self.http_protocol}://{self.domain_host_name}:{self.port}'
    
    @property
    def api_v1_url(self) -> str:
        return f'{self.web_url}{self.api_v1_prefix}'

    class Config:
        env_file = '.env'


settings = Settings()
