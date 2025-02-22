from pydantic import BaseModel


class RecognizeResponse(BaseModel):
    title: str | None
    album: str | None
    author: str | None
    url: str | None
    recognized: bool
