from sqlalchemy.orm import Session
import models, schemas


def create_item(db: Session, item: schemas.ItemCreate):
    try:
        db_item = models.Item(**item.dict())
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except:
        db.rollback()
        raise


def get_items(db: Session):
    return db.query(models.Item).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def update_item(db: Session, item_id: int, item: schemas.ItemCreate):
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    try:
        for key, value in item.dict().items():
            setattr(db_item, key, value)

        db.commit()
        db.refresh(db_item)
        return db_item
    except:
        db.rollback()
        raise


def delete_item(db: Session, item_id: int):
    db_item = get_item(db, item_id)
    if not db_item:
        return None

    try:
        db.delete(db_item)
        db.commit()
        return db_item
    except:
        db.rollback()
        raise
