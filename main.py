from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field, validator
from typing import Optional

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
def home():
    return {"message": "Welcome to FastAPI demo"}

@app.post("/items")
def create_item(item: Item):
    item_id = len(items_db) + 1
    items_db[item_id] = item

    return {
        "message": "Item created successfully",
        "item_id": item_id,
        "data": item
    }

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Path(..., gt=0),
    include_description: bool = Query(False)
):
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
def update_item(item_id: int, item: Item):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db[item_id] = item

    return {
        "message": "Item updated successfully",
        "data": item
    }

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]

    return {
        "message": "Item deleted successfully"
    }
