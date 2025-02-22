from datetime import datetime
from fastapi import FastAPI, UploadFile, File

from .schemas import RecognizeResponse


app = FastAPI()


started_time = datetime.now()


@app.get('/')
async def main() -> dict:
    return {'started_time': started_time, 'time': datetime.now()}


@app.post('/recognize', response_model=RecognizeResponse)
async def recognize(
    audio: UploadFile = File(media_type='audio/wav')
) -> RecognizeResponse:
    return RecognizeResponse(
        title=None, album=None, author=None,
        url=None, recognized=False)
