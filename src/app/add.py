"""
    Add song to database.
"""

from typing import Sequence
from sqlalchemy import select

from database import create_session
from tables import AuthorTable, SongTable
from schemas import AuthorBase, SongBase


def get_all_authors() -> Sequence[AuthorTable]:
    with create_session() as session:
        authors = session.scalars(select(AuthorTable)).all()
        return authors
    
    
def get_all_songs() -> Sequence[SongTable]:
    with create_session() as session:
        songs = session.scalars(select(SongTable)).all()
        return songs


def add_author(author_metadata: AuthorBase):
    with create_session() as session:
        session.add(AuthorTable(**author.model_dump()))
        session.commit()
        

def add_song(audio: bytes, song_metadata: SongBase):
    with create_session() as session:
        session.add(SongTable(**song.model_dump()))
        session.commit()
