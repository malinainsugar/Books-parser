from sqlalchemy import Column, Integer, String
from .database import Base


class Novelty(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    author = Column(String)
    publisher = Column(String)
    year = Column(Integer)
    page_count = Column(Integer)
    price = Column(Integer)
    description = Column(String)
    link = Column(String)
    product_id = Column(Integer)


