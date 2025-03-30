from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import FastAPI, UploadFile, File

from .schemas import RecognizeResponse
from actions import lifespan
from database import get_async_db_session


app = FastAPI(lifespan=lifespan)


started_time = datetime.now()


@app.get('/')
async def main() -> dict:
    return {'started_time': started_time, 'time': datetime.now()}


@app.post('/recognize', response_model=RecognizeResponse)
async def recognize(
    async_db_session: get_async_db_session,
    audio_file: UploadFile = File(media_type='audio/wav'),
) -> RecognizeResponse:
    
    return RecognizeResponse(
        title=None, album=None, author=None,
        url=None, recognized=False)
