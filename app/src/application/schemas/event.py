from datetime import datetime

from pydantic import BaseModel


class Event(BaseModel):
    sport: str
    description: str
    start_date: datetime
    end_date: datetime


class EventInDB(Event):
    id: int

    class Config:
        from_attributes = True
