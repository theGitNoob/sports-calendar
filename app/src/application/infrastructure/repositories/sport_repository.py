from sqlalchemy.orm import Session

from app.src.application.infrastructure.models.sport_model import SportDAO, incompatible_sports_table
from app.src.application.schemas.sport import Sport, SportDTO, SportDTOInDB, SportInDB


def create_sport(db: Session, sport: SportDTO):
    sport_search = db.query(SportDAO).filter(sport.name == SportDAO.name).first()
    if sport_search is not None:
        raise Exception("Sport already exists")

    sport_to_create = Sport(**sport.dict())
    db_sport = SportDAO(**sport_to_create.model_dump())
    db.add(db_sport)
    db.commit()
    db.refresh(db_sport)

    for incompatible_sport_name in sport.incompatible_sports:
        incompatible_sport = db.query(SportDAO).filter_by(name=incompatible_sport_name).first()
        if incompatible_sport:
            db_sport.add_incompatible_sport(incompatible_sport)

    db.commit()

    return db_sport


def get_sport_by_id(db: Session, sport_id: int):
    sport = db.query(SportDAO).filter(SportDAO.id == sport_id).first()

    if sport:
        incompatible_sports_as_minor = [incompatible.name for incompatible in sport.incompatible_sports]

        incompatible_sports_as_major = db.query(SportDAO).join(
            incompatible_sports_table,
            SportDAO.id == incompatible_sports_table.c.sport_id
        ).filter(incompatible_sports_table.c.incompatible_sport_id == sport_id).all()

        incompatible_sports_as_major_names = [sport.name for sport in incompatible_sports_as_major]

        all_incompatible_sports = incompatible_sports_as_minor + incompatible_sports_as_major_names

        sport_dto = SportDTOInDB(
            id=sport_id,
            name=sport.name,
            zone=sport.zone,
            incompatible_sports=all_incompatible_sports
        )
        return sport_dto

    return None


def get_simple_sport_by_id(db: Session, sport_id: int):
    sport = db.query(SportDAO).filter(SportDAO.id == sport_id).first()
    if sport is None:
        raise Exception("Sport not Found")

    return sport


def get_all_sports(db: Session):
    return db.query(SportDAO).all()


def clean_incompatible_sports(db: Session, sport_id: int):
    sport = get_simple_sport_by_id(db, sport_id)
    if sport:
        db.query(incompatible_sports_table).filter(
            incompatible_sports_table.c.sport_id == sport_id
        ).delete(synchronize_session=False)

        db.query(incompatible_sports_table).filter(
            incompatible_sports_table.c.incompatible_sport_id == sport_id
        ).delete(synchronize_session=False)

        db.commit()


def update_sport(db: Session, sport_id: int, sport: SportDTO):
    db_sport = get_simple_sport_by_id(db, sport_id)
    db_sport.name = sport.name
    db_sport.zone = sport.zone
    if sport.incompatible_sports is not None:
        clean_incompatible_sports(db, sport_id)
        for incompatible_sport in sport.incompatible_sports:
            incompatible_sport = db.query(SportDAO).filter(SportDAO.name == incompatible_sport).first()
            if incompatible_sport is None:
                raise Exception("Incompatible sport not found")
            if incompatible_sport not in db_sport.incompatible_sports:
                db_sport.add_incompatible_sport(incompatible_sport)
    db.commit()
    db.refresh(db_sport)
    return SportInDB(id=sport_id, name=db_sport.name, zone=db_sport.zone)


def delete_sport(db: Session, sport_id: int):
    db_sport = get_simple_sport_by_id(db, sport_id)
    db.delete(db_sport)
    db.commit()
