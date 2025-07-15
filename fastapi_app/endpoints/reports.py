from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from fastapi_app import crud, schemas, database

router = APIRouter()

@router.get("/image-detections/", response_model=List[schemas.ImageDetection])
def read_image_detections(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_image_detections(db=db, skip=skip, limit=limit)
