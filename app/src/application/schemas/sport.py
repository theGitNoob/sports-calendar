from pydantic import BaseModel


class SportDTO(BaseModel):
    name: str
    zone: str
    incompatible_sports: list[str]


class Sport(BaseModel):
    name: str
    zone: str


class SportInDB(Sport):
    id: int

    class Config:
        from_attributes = True


class SportDTOInDB(SportDTO):
    id: int

    class Config:
        from_attributes = True
