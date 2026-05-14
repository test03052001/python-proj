from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str


class PaginationParams(BaseModel):
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=100, ge=1, le=500)
