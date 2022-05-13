from pydantic import BaseModel, Field


class StatusPydantic(BaseModel):
    message: str


class PaginationPydantic(BaseModel):
    offset: int = Field(default=0)
    limit: int = Field(default=100)
