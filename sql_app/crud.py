import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_book(db: Session, book_id: int):
    return db.query(models.Novelty).filter(models.Novelty.product_id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Novelty).offset(skip).limit(limit).all()

def create_book(db: Session, item: schemas.NoveltyCreate):
    db_book = models.Novelty(
        name=item.name,
        author = item.author,
        publisher = item.publisher,
        year = item.year,
        page_count = item.page_count,
        price = item.price,
        description = item.description,
        link = item.link,
        product_id = item.product_id
    )
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, item: schemas.NoveltyUpdate, book_id: int):
    db_item = get_book(db, book_id=book_id)
    db_item.name = item.name
    db_item.author = item.author
    db_item.publisher = item.publisher
    db_item.year = item.year
    db_item.page_count = item.page_count
    db_item.price = item.price
    db_item.description = item.description
    db_item.link = item.link
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_book(db: Session, book_id: int):
    db_item = get_book(db, book_id=book_id)
    db.delete(db_item)
    db.commit()
