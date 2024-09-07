from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import AbstractUser, TimestampedMixin


class User(AbstractUser, TimestampedMixin):
    """Модель пользователя"""
    telegram_id: Mapped[Optional[int]] = mapped_column(
        index=True,
        unique=True,
        nullable=True,
        default=None,
    )
    
    notes = relationship('Note', back_populates='owner')




    




