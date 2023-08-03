from pydantic import BaseModel


class NoveltyBase(BaseModel):
    name: str
    author : str
    publisher : str 
    year : int
    pageСount : int
    price : int
    description : str 
    link : str 


class NoveltyCreate(NoveltyBase):
    pass


class Novelty(NoveltyBase):
    id: int

    class Config:
        orm_mode = True
