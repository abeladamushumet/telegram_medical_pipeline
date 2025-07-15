from sqlalchemy.orm import Session
from fastapi_app import models, schemas
from typing import List

def get_image_detections(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.ImageDetection]:
    return db.query(models.ImageDetection).offset(skip).limit(limit).all()

def get_messages(db: Session, skip: int = 0, limit: int = 100) -> List[schemas.TelegramMessage]:
    return db.query(models.TelegramMessage).offset(skip).limit(limit).all()
