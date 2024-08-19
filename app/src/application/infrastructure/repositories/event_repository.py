from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.src.application.infrastructure.models import SportDAO
from app.src.application.infrastructure.models.event_model import EventDAO
from app.src.application.infrastructure.models.sport_model import incompatible_sports_table
from app.src.application.schemas.event import EventDTO


def create_event(db: Session, event: EventDTO):
    sport = db.query(SportDAO).filter(SportDAO.name == event.sport).first()
    if not sport:
        raise ValueError(f"El deporte {event.sport} no existe.")

    incompatible_sports_ids = {incompatible.id for incompatible in sport.incompatible_sports}

    incompatible_with_sport_ids = db.query(incompatible_sports_table.c.sport_id).filter(
        incompatible_sports_table.c.incompatible_sport_id == sport.id
    ).all()
    incompatible_with_sport_ids = {item[0] for item in incompatible_with_sport_ids}

    all_incompatible_ids = incompatible_sports_ids.union(incompatible_with_sport_ids)

    conflicting_event = db.query(EventDAO).filter(
        EventDAO.sport_id.in_(all_incompatible_ids),
        and_(
            EventDAO.start_date <= event.end_date,
            EventDAO.end_date >= event.start_date
        )
    ).first()

    if conflicting_event:
        raise ValueError(
            f"Existe un conflicto con un deporte incompatible ({conflicting_event.sport.name}) programado en el mismo rango de fechas ({conflicting_event.start_date} - {conflicting_event.end_date}).")

    overlapping_event = db.query(EventDAO).join(SportDAO).filter(
        SportDAO.zone == sport.zone,
        and_(
            EventDAO.start_date <= event.end_date,
            EventDAO.end_date >= event.start_date
        )
    ).first()

    if overlapping_event:
        raise ValueError(
            f"Ya existe un evento en la zona {sport.zone} que se solapa con el intervalo de tiempo del nuevo evento ({event.start_date} - {event.end_date}).")

    db_event = EventDAO(
        description=event.description,
        start_date=event.start_date,
        end_date=event.end_date,
        sport_id=sport.id,
        gender=event.gender
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    response = {
        "id": db_event.id,
        "sport": sport.name,
        "description": db_event.description,
        "start_date": db_event.start_date,
        "end_date": db_event.end_date,
        "gender": db_event.gender
    }
    return response


def get_event_by_id(db: Session, event_id: int):
    return db.query(EventDAO).filter(EventDAO.id == event_id).first()


def get_all_events(db: Session):
    return db.query(EventDAO).all()


def update_event(db: Session, event_id: int, event: EventDTO):
    sport = db.query(SportDAO).filter(SportDAO.name == event.sport).first()
    if not sport:
        raise ValueError(f"El deporte {event.sport} no existe.")

    incompatible_sports_ids = {incompatible.id for incompatible in sport.incompatible_sports}

    incompatible_with_sport_ids = db.query(incompatible_sports_table.c.sport_id).filter(
        incompatible_sports_table.c.incompatible_sport_id == sport.id
    ).all()
    incompatible_with_sport_ids = {item[0] for item in incompatible_with_sport_ids}

    all_incompatible_ids = incompatible_sports_ids.union(incompatible_with_sport_ids)

    conflicting_event = db.query(EventDAO).filter(
        EventDAO.sport_id.in_(all_incompatible_ids),
        and_(
            EventDAO.start_date <= event.end_date,
            EventDAO.end_date >= event.start_date
        )
    ).first()

    if conflicting_event:
        raise ValueError(
            f"Existe un conflicto con un deporte incompatible ({conflicting_event.sport.name}) programado en el mismo rango de fechas ({conflicting_event.start_date} - {conflicting_event.end_date}).")

    overlapping_event = db.query(EventDAO).join(SportDAO).filter(
        SportDAO.zone == sport.zone,
        and_(
            EventDAO.start_date <= event.end_date,
            EventDAO.end_date >= event.start_date
        ),
        and_(EventDAO.id != event_id)
    ).first()

    if overlapping_event:
        raise ValueError(
            f"Ya existe un evento en la zona {sport.zone} que se solapa con el intervalo de tiempo del nuevo evento ({event.start_date} - {event.end_date}).")

    db_event = get_event_by_id(db, event_id)
    sport = db.query(SportDAO).filter(SportDAO.name == event.sport).first()
    if not sport:
        raise ValueError(f"El deporte {event.sport} no existe.")
    db_event.sport = sport
    db_event.description = event.description
    db_event.start_date = event.start_date
    db_event.end_date = event.end_date
    db_event.gender = event.gender
    db.commit()
    db.refresh(db_event)
    return db_event


def delete_event(db: Session, event_id: int):
    db_event = get_event_by_id(db, event_id)
    db.delete(db_event)
    db.commit()
    return db_event
