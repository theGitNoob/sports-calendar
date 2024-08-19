from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.src.application.infrastructure.db import Base

incompatible_sports_table = Table('incompatible_sports', Base.metadata,
                                  Column('sport_id', Integer, ForeignKey('sports.id'), primary_key=True),
                                  Column('incompatible_sport_id', Integer, ForeignKey('sports.id'), primary_key=True))


class SportDAO(Base):
    __tablename__ = "sports"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    zone = Column(String, nullable=False)

    events = relationship("EventDAO", back_populates="sport", cascade="all, delete-orphan")
    incompatible_sports = relationship("SportDAO", secondary=incompatible_sports_table,
                                       primaryjoin=id == incompatible_sports_table.c.sport_id,
                                       secondaryjoin=id == incompatible_sports_table.c.incompatible_sport_id,
                                       backref="incompatible_with")

    def __repr__(self):
        return f"<Sport(name={self.name})>"

    def add_incompatible_sport(self, sport):
        if self.id < sport.id:
            self.incompatible_sports.append(sport)
        else:
            sport.incompatible_sports.append(self)
