from sqlalchemy import Column, Integer, String, DateTime

from app.src.application.infrastructure.db import Base


class EventDAO(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    sport = Column(String, index=True)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
