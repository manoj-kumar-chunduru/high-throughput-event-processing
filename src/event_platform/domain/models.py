from typing import Any

from pydantic import BaseModel, Field


class Event(BaseModel):
    event_id: str = Field(min_length=1)
    key: str = Field(min_length=1)
    event_type: str = Field(min_length=1)
    payload: dict[str, Any]


class PublishResponse(BaseModel):
    event_id: str
    partition: int
    accepted: bool
