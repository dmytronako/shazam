from __future__ import annotations
from sqlalchemy import Integer, VARCHAR, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class AuthorTable(Base):
    __tablename__ = 'authors'
    
    author_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(256), nullable=False)
    songs: Mapped[list[SongTable]] = relationship(back_populates='author')


class SongTable(Base):
    __tablename__ = 'songs'
    
    song_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(VARCHAR(256))
    album: Mapped[str] = mapped_column(VARCHAR(256), nullable=True)
    author_id: Mapped[str] = mapped_column(ForeignKey('authors.author_id'))
    author: Mapped[AuthorTable] = relationship(back_populates='songs')
