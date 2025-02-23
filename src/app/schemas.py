from pydantic import BaseModel, Field


class RecognizeResponse(BaseModel):
    """
        Response to recognize request.
    """
    
    title: str | None = Field(..., ge=1, le=256, description='Title of the song.')
    album: str | None = Field(..., ge=1, le=256, description='Album the song belongs to.')
    author: str | None = Field(..., ge=1, le=256, description='Author of the song.')
    url: str | None = Field(..., ge=1, le=256, description='Url to the song.')
    recognized: bool = Field(..., description='If the song is found in database.')
