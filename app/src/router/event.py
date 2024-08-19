from typing import List

from fastapi import HTTPException, Body, Depends, APIRouter

from app.src.application.infrastructure.db import get_db
from app.src.application.infrastructure.repositories.event_repository import *
from app.src.application.schemas.event import EventInDB, EventDTOInDB

router = APIRouter(
    tags=["events"],
    responses={404: {"description": "Not found"}},
    prefix="/events"
)


@router.post("/", response_model=EventDTOInDB, status_code=201)
async def create(event: EventDTO, db: Session = Depends(get_db)):
    try:
        return create_event(db, event)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{event_id}", status_code=204)
def delete(event_id: int, db: Session = Depends(get_db)):
    try:
        deleted_event = delete_event(db, event_id)
        if deleted_event is None:
            raise HTTPException(status_code=404, detail="Event not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{event_id}", response_model=EventInDB, status_code=201)
def update(event_id: int, event: EventDTO = Body(..., description="The updated event object"),
           db: Session = Depends(get_db)):
    try:
        updated_event = update_event(db, event_id, event)
        if updated_event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return updated_event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{event_id}", response_model=EventInDB)
def read_single(event_id: int, db: Session = Depends(get_db)):
    try:
        event = get_event_by_id(db, event_id)
        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")
        return event
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[EventInDB])
def read_all(db: Session = Depends(get_db)):
    try:
        return get_all_events(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
