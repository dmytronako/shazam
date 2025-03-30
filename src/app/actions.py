from typing import Sequence
from io import BytesIO
from contextlib import asynccontextmanager
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import librosa
from fastapi import FastAPI

from database import init_db
from tables import HashedSongsTable
from core import create_constellation_map, create_combinatorial_hashing


MIN_AUDIO_DURATION = 5  # Minimal audio duration.
MAX_AUDIO_DURATION = 15  # Maximal audio duration.
SAMPLE_RATE = 16_000  # Sample rate for audio.


@asynccontextmanager
def lifespan(app: FastAPI):
    init_db()
    yield
    
    
async def get_hashes_db(
    async_db_session: AsyncSession, audio_hashes: Sequence
) -> Sequence[HashedSongsTable]:
    db_hashes = await async_db_session.scalars(
        select(HashedSongsTable).where(
            HashedSongsTable.song_id.in_(audio_hashes)))
    return db_hashes
    
    
async def recognize_song(async_db_session: AsyncSession, audio_file: BytesIO):   
    audio, sample_rate = librosa.load(audio_file, sr=SAMPLE_RATE, mono=True)
    audio_duration = audio.size / sample_rate
    
    if audio_duration < MIN_AUDIO_DURATION or MAX_AUDIO_DURATION < audio_duration:
        raise ValueError(
            f'Duration of audio must be from {MIN_AUDIO_DURATION}'
            f'to {MAX_AUDIO_DURATION}, meanwhile duration of the audio is {audio_duration}.')

    constellation_map = create_constellation_map(audio, SAMPLE_RATE)
    combinatorial_hashing = create_combinatorial_hashing(constellation_map)
    hashed_db = await get_hashes_db(async_db_session, combinatorial_hashing.keys())
