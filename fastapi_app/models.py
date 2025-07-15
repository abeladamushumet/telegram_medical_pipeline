from sqlalchemy import Column, Integer, BigInteger, String, Float, TIMESTAMP
from fastapi_app.database import Base

class ImageDetection(Base):
    __tablename__ = "image_detections"

    id = Column(BigInteger, primary_key=True, index=True)
    image_id = Column(BigInteger, index=True)
    detection_label = Column(String)
    confidence = Column(Float)
    detected_at = Column(TIMESTAMP)

class TelegramMessage(Base):
    __tablename__ = "fct_messages"

    message_id = Column(BigInteger, primary_key=True, index=True)
    message_date = Column(TIMESTAMP)
    message_text = Column(String)
    views = Column(Integer)
    replies_count = Column(Integer)
    post_author = Column(String)
    grouped_id = Column(BigInteger)
