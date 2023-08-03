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



# @app.get("/prices/", response_model=list[schemas.Price])
# def read_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     prices = crud.get_prices(db, skip=skip, limit=limit)
#     return prices

# @app.get("/prices/{price_id}", response_model=schemas.Price)
# def read_price(price_id: int, db: Session = Depends(get_db)):
#     db_price = crud.get_price_by_id(db, price_id=price_id)
#     if db_price is None:
#         raise HTTPException(status_code=404, detail='Элемент не найден')
#     return db_price

# @app.post("/prices/create", response_model=schemas.Price)
# def create_price(item: schemas.PriceCreate, db: Session = Depends(get_db)):
#     db_price = crud.get_price_by_name(db, name=item.name)
#     if db_price and db_price.price == item.price:
#         raise HTTPException(status_code=400, detail='Элемент с таким названием уже существует')
#     return crud.create_price(db=db, item=item)

# @app.put("/prices/{price_id}", response_model=schemas.Price)
# def update_price(price_id: int, item: schemas.PriceCreate, db: Session = Depends(get_db)):
#     db_price = crud.get_price_by_id(db, price_id=price_id)
#     if not db_price:
#         raise HTTPException(status_code=400, detail='Элемент не найден')
#     return crud.update_price(db=db, item=item, price_id=price_id)

# @app.delete("/prices/{price_id}", response_model=dict)
# def delete_price(price_id: int, db: Session = Depends(get_db)):
#     db_price = crud.get_price_by_id(db, price_id=price_id)
#     if not db_price:
#         raise HTTPException(status_code=400, detail='Элемент не найден')
#     crud.delete_price(db=db, price_id=price_id)
#     return {'status':'Элемент удален'}

# if __name__ == "__main__":
#     asyncio.run(main())