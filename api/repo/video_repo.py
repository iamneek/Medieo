from sqlalchemy.orm import Session
from api.models.video import Video
from api.schemas import Video as VideoSchema


def create_video(db: Session, upload_id: str, title: str, description: str):
    existing = db.query(Video).filter(Video.upload_id == upload_id).first()
    if not existing:
        video = Video(upload_id=upload_id, title=title, description=description)
        db.add(video)
        db.commit()
        db.refresh(video)
        return video
    
def get_all_videos(db: Session, page: int = 1, limit: int = 10):
    videos = db.query(Video).offset((page - 1) * limit).limit(limit).all()
    total = db.query(Video).count()
    return {'videos':  [VideoSchema.model_validate(v) for v in videos], 'total': total, 'page': page, 'limit': limit}