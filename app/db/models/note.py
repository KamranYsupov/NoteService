from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base, TimestampedMixin


class Note(Base, TimestampedMixin):
    title: Mapped[str] = mapped_column(index=True)
    content: Mapped[str] = mapped_column()
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    tags: Mapped[list['Tag']] = relationship(
        'Tag',
        secondary='note_tags', 
        back_populates='notes',
        lazy='selectin',
    )
    owner: Mapped['User'] = relationship('User', back_populates='notes') 