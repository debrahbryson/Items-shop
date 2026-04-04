from sqlalchemy.orm import Session
import models, schemas
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate):
    try:
        hashed_password = get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating user: {e}")

def get_user_by_email(db: Session, email: str):
    try:
        return db.query(models.User).filter(models.User.email == email).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}")

def get_user_by_username(db: Session, username: str):
    try:
        return db.query(models.User).filter(models.User.username == username).first()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}")

def get_user(db: Session, user_id: int):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user: {e}")

def get_users(db: Session, skip: int = 0, limit: int = 100):
    try:
        return db.query(models.User).offset(skip).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching users: {e}")

def create_item(db: Session, item: schemas.ItemCreate):
    try:
        db_item = models.Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating item: {e}")

def get_items(db: Session):
    try:
        return db.query(models.Item).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching items: {e}")

def get_item(db: Session, item_id: int):
    try:
        item = db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Item not found")
        return item
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching item: {e}")

def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    try:
        db_item = get_item(db, item_id)
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        db.commit()
        db.refresh(db_item)
        return db_item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating item: {e}")

def delete_item(db: Session, item_id: int):
    try:
        db_item = get_item(db, item_id)
        db.delete(db_item)
        db.commit()
        return db_item
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting item: {e}")
