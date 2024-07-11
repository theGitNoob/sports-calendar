from sqlalchemy.orm import Session

from app.src.application.infrastructure.models.event_model import EventDAO
from app.src.application.schemas.event import Event


def create_event(db: Session, event: Event):
    db_event = EventDAO(**event.model_dump())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def get_event_by_id(db: Session, event_id: int):
    return db.query(EventDAO).filter(EventDAO.id == event_id).first()


def get_all_events(db: Session):
    return db.query(EventDAO).all()


def update_event(db: Session, event_id: int, event: Event):
    db_event = get_event_by_id(db, event_id)
    db_event.sport = event.sport
    db_event.description = event.description
    db_event.start_date = event.start_date
    db_event.end_date = event.end_date
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = get_event_by_id(db, event_id)
    db.delete(db_event)
    db.commit()
    return db_event
