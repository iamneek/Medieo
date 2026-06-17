from fastapi import APIRouter
from storage.s3 import s3_get_presigned_url

router = APIRouter()


@router.get("/watch/{upload_id}")
async def stream(upload_id):
    stream_url = s3_get_presigned_url(key=f"videos/{upload_id}/index.m3u8")
    return {"stream_url": stream_url}
