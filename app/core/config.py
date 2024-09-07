from enum import Enum

from pydantic import Field
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
    log_level: LogLevel = Field(title='Уровень логирования', default=LogLevel.INFO)  
    
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
            'app.api.v1.endpoints.user',
            'app.api.v1.endpoints.auth',
            'app.api.v1.deps',
        ]
    )

    @property
    def db_url(self) -> str:
        return self.sqlite_default_url

    class Config:
        env_file = '.env'


settings = Settings()
