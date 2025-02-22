from fastapi import FastAPI, UploadFile, File

from .schemas import RecognizeResponse


app = FastAPI()


@app.post('/recognize', response_model=RecognizeResponse)
async def recognize(
    audio: UploadFile = File(media_type='audio/wav')
) -> RecognizeResponse:
    return RecognizeResponse(
        title=None, album=None, author=None,
        url=None, recognized=False)
