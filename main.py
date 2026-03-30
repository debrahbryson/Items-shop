from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio

import models, schemas, crud
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def home():
    await asyncio.sleep(2)
    return {"message": "Welcome to FastAPI demo"}

@app.post("/items", response_model=schemas.ItemResponse)
async def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    return crud.create_item(db, item)

@app.get("/items", response_model=list[schemas.ItemResponse])
async def list_items(db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    return crud.get_items(db)

@app.get("/items/{item_id}", response_model=schemas.ItemResponse)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    db_item = crud.get_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.put("/items/{item_id}", response_model=schemas.ItemResponse)
async def update_item(item_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    db_item = crud.update_item(db, item_id, item)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@app.delete("/items/{item_id}")
async def delete_item(item_id: int, db: Session = Depends(get_db)):
    await asyncio.sleep(2)
    db_item = crud.delete_item(db, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
