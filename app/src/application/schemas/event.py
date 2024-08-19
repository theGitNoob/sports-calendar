from datetime import datetime

from pydantic import BaseModel

from app.src.application.schemas.sport import Sport


class EventDTO(BaseModel):
    sport: str
    description: str
    start_date: datetime
    end_date: datetime
    gender: str


class Event(BaseModel):
    sport: Sport
    description: str
    start_date: datetime
    end_date: datetime
    gender: str


class EventInDB(Event):
    id: int

    class Config:
        from_attributes = True


class EventDTOInDB(EventDTO):
    id: int

    class Config:
        from_attributes = True
