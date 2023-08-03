from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import asyncio
import uvicorn

# uvicorn sql_app.main:app --reload

from . import crud, models, schemas
from .database import SessionLocal, engine
# from .parser_price import start_parser

# Create Rocketry app
from rocketry import Rocketry

app_rocketry = Rocketry(execution="async")


# Create some tasks
# @app_rocketry.task('every 15 seconds')
# async def do_things():
#     print('Start parser')
#     name, price = start_parser()
#     import requests

#     def blocking_task():
#         headers = {
#             'accept': 'application/json',
#             'Content-Type': 'application/json',
#         }

#         json_data = {
#             'name': name,
#             'price': price,
#         }
#         response = requests.post('http://127.0.0.1:8000/prices/create', headers=headers, json=json_data)


#     loop = asyncio.get_running_loop()
#     awaitable = loop.run_in_executor(None, blocking_task)



models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# @app.on_event("startup")
# async def startup_event():
#     asyncio.create_task(app_rocketry.serve())



@app.get("/books", response_model=list[schemas.Novelty])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db, skip=skip, limit=limit)
    return books

@app.get("/books/{book_id}", response_model=schemas.Novelty)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail='Элемент не найден')
    return db_book

@app.post("/books/create", response_model=schemas.Novelty)
def create_book(item: schemas.NoveltyCreate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=item.product_id)
    if db_book:
        raise HTTPException(status_code=400, detail='Такой элемент уже существует')
    return crud.create_book(db=db, item=item)

@app.put("/books/{book_id}", response_model=schemas.Novelty)
def update_book(book_id: int, item: schemas.NoveltyUpdate, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail='Элемент не найден')
    return crud.update_book(db=db, item=item, book_id=book_id)

@app.delete("/books/{book_id}", response_model=str)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id=book_id)
    if not db_book:
        raise HTTPException(status_code=400, detail='Элемент не найден')
    crud.delete_book(db=db, book_id=book_id)
    return 'Элемент удален'

# if __name__ == "__main__":
#     asyncio.run(main())