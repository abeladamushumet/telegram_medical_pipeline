from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ImageDetectionBase(BaseModel):
    image_id: int
    detection_label: str
    confidence: float
    detected_at: datetime

class ImageDetectionCreate(ImageDetectionBase):
    pass

class ImageDetection(ImageDetectionBase):
    id: int

    class Config:
        orm_mode = True

class TelegramMessageBase(BaseModel):
    message_id: int
    message_date: datetime
    message_text: str
    views: Optional[int]
    replies_count: Optional[int]
    post_author: Optional[str]
    grouped_id: Optional[int]

class TelegramMessage(TelegramMessageBase):
    class Config:
        orm_mode = True
