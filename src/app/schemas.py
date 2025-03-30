from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    """
        Base class for author.
    """
    name: str
    
    
class SongBase(BaseModel):
    """
        Base class for song.
    """
    title: str = Field(..., min_length=1, max_length=255)
    album: str | None = Field(..., min_length=1, max_length=255)
    author_id: int


class RecognizeResponse(BaseModel):
    """
        Response to recognize request.
    """
    
    title: str | None = Field(..., ge=1, le=256, description='Title of the song.')
    album: str | None = Field(..., ge=1, le=256, description='Album the song belongs to.')
    author: str | None = Field(..., ge=1, le=256, description='Author of the song.')
    url: str | None = Field(..., ge=1, le=256, description='Url to the song.')
    recognized: bool = Field(..., description='If the song is found in database.')
