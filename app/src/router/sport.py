from typing import List

from fastapi import HTTPException, Depends, APIRouter

from app.src.application.infrastructure.db import get_db
from app.src.application.infrastructure.repositories.sport_repository import *
from app.src.application.schemas.sport import SportInDB, SportDTOInDB

router = APIRouter(
    tags=["sports"],
    responses={404: {"description": "Not found"}},
    prefix="/sports"
)


@router.post("/", response_model=SportInDB, status_code=201)
async def create(sport: SportDTO, db: Session = Depends(get_db)):
    try:
        return create_sport(db, sport)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{sport_id}", status_code=204)
async def delete(sport_id: int, db: Session = Depends(get_db)):
    try:
        deleted_sport = delete_sport(db, sport_id)
        if deleted_sport is None:
            raise HTTPException(status_code=404, detail="Sport not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{sport_id}", response_model=SportInDB, status_code=201)
async def update(sport_id: int, sport: SportDTO,
                 db: Session = Depends(get_db)):
    try:
        updated_sport = update_sport(db, sport_id, sport)
        if updated_sport is None:
            raise HTTPException(status_code=404, detail="Sport not found")
        return updated_sport
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{sport_id}", response_model=SportDTOInDB)
async def read_single(sport_id: int, db: Session = Depends(get_db)):
    try:
        sport = get_sport_by_id(db, sport_id)
        if sport is None:
            raise HTTPException(status_code=404, detail="Sport not found")
        return sport
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[SportInDB])
async def read_all(db: Session = Depends(get_db)):
    try:
        return get_all_sports(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
