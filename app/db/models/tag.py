from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_mixins import Base


class Tag(Base):
    name: Mapped[str] = mapped_column(unique=True)

    notes: Mapped[list['Note']] = relationship(
        'Note', 
        secondary='note_tags', 
        back_populates='tags'
    )
    
    
class NoteTag(Base):
    __tablename__ = 'note_tags'

    note_id: Mapped[int] = mapped_column(ForeignKey('notes.id'), primary_key=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey('tags.id'), primary_key=True)


