from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional
import asyncio

app = FastAPI()

class Item(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    price: float = Field(..., gt=0)
    quantity: int = Field(default=1, ge=1)
    description: Optional[str] = None

    @validator("name")
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Name cannot be empty")
        return value

items_db = {}

@app.get("/")
async def home():
    await asyncio.sleep(2)
    return {"message": "Welcome to FastAPI demo"}

@app.post("/items")
async def create_item(item: Item):
    await asyncio.sleep(2)
    item_id = len(items_db) + 1
    items_db[item_id] = item

    return {
        "message": "Item created successfully",
        "item_id": item_id,
        "data": item
    }

@app.get("/items")
async def list_items():
    await asyncio.sleep(2)
    return {item_id: item for item_id, item in items_db.items()}

@app.get("/items/{item_id}")
async def get_item(
    item_id: int = Path(..., gt=0),
    include_description: bool = Query(False)
):
    await asyncio.sleep(2)

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items_db[item_id]

    response = {
        "name": item.name,
        "price": item.price,
        "quantity": item.quantity
    }

    if include_description:
        response["description"] = item.description

    return response

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    await asyncio.sleep(2)

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db[item_id] = item

    return {
        "message": "Item updated successfully",
        "data": item
    }

@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    await asyncio.sleep(2)

    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]

    return {
        "message": "Item deleted successfully"
    }
