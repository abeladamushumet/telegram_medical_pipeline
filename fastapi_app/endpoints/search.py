from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from fastapi_app import crud, schemas, database

router = APIRouter()

@router.get("/messages/", response_model=List[schemas.TelegramMessage])
def search_messages(
    q: str = Query(..., min_length=3, description="Search query text"),
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(database.get_db),
):
    # Simple text search in message_text
    query = db.query(schemas.TelegramMessage).filter(schemas.TelegramMessage.message_text.ilike(f"%{q}%"))
    results = query.offset(skip).limit(limit).all()
    return results
