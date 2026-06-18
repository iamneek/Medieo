from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from pydantic import ConfigDict


class Video(BaseModel):
    upload_id: str
    title: str
    description: Optional[str]
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)
