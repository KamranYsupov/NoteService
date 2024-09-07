from dependency_injector import containers, providers

from app.repositories import (
    RepositoryUser,
    RepositoryRefreshToken,
    RepositoryNote, 
    RepositoryTag,
)
from app.services import (
    UserService,
    JWTService,
    NoteService,
    TagService,
    TelegramBotService,
)
from app.db import (
    DataBaseManager,
    User,
    RefreshToken,
    Note,
    Tag,
)
from app.core.config import settings


class Container(containers.DeclarativeContainer):
    db_manager = providers.Singleton(DataBaseManager, db_url=settings.db_url)
    session = providers.Resource(db_manager().get_async_session)

    # region repository
    repository_user = providers.Singleton(
        RepositoryUser, model=User, session=session
    )
    repository_note = providers.Singleton(
        RepositoryNote, model=Note, session=session
    )
    repository_tag = providers.Singleton(
        RepositoryTag, model=Tag, session=session
    )
    repository_refresh_token = providers.Singleton(
        RepositoryRefreshToken, model=RefreshToken, session=session
    )
    # endregion

    # region services
    note_service = providers.Singleton(
        NoteService,
        repository_note=repository_note,
        repository_tag=repository_tag,
    )
    tag_service = providers.Singleton(
        TagService, 
        repository_tag=repository_tag,
        unique_fields=('name'),
    )
    jwt_service = providers.Singleton(
        JWTService, repository_refresh_token=repository_refresh_token
    )
    telegram_service = providers.Singleton(
        TelegramBotService, bot_token=settings.bot_token
    )
    user_service = providers.Singleton(
        UserService, 
        repository_user=repository_user, 
        telegram_service=telegram_service,
        unique_fields=('telegram_id', 'username', 'email')
    )
    # endregion


container = Container()
container.init_resources()
container.wire(modules=settings.container_wiring_modules)
