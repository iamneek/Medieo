from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Video(BaseModel):
    upload_id: str
    title: str
    description: Optional[str]
    uploaded_at: datetime
