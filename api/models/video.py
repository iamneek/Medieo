from sqlalchemy import Column, String, Text, DateTime, func

from ..database import Base


class Video(Base):
    __tablename__ = "video"
    upload_id = Column(String(40), primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
