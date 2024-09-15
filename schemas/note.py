from pydantic import BaseModel

class CreateNote(BaseModel):
    title: str
    content: str
    tags: list[str] = []

class SearchByTags(BaseModel):
    tags: list[str]