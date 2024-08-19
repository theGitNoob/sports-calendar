from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.src.application.infrastructure.db import Base


class EventDAO(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    gender = Column(String)
    sport_id = Column(Integer, ForeignKey("sports.id"), nullable=False)

    sport = relationship("SportDAO", back_populates="events")

    def __repr__(self):
        return f"<Event(description={self.description}, start_date={self.start_date}, end_date={self.end_date})>"
