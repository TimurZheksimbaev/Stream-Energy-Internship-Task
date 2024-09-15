from pydantic import BaseModel, Field

class CreateNote(BaseModel):
    title: str = Field(..., max_length=100, min_length=1)
    content: str = Field(..., min_length=1)
    tags: list[str] = Field(...)


class SearchByTags(BaseModel):
    tags: list[str]