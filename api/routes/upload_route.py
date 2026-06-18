from fastapi import APIRouter, UploadFile, File, Form, status, Depends, HTTPException
import uuid
from fastapi.responses import JSONResponse
import os
import tempfile
from tasks.transcoding import transcode_t_hls
from api.database import get_db
from sqlalchemy.orm import Session
from api.repo.video_repo import create_video
from api.models.video import Video

router = APIRouter()


@router.post("/upload/init")
async def upload_init():
    up_id = str(uuid.uuid4())
    return JSONResponse({"upload_id": up_id}, status_code=status.HTTP_201_CREATED)


@router.post("/upload/")
async def upload_video(
    up_id: str = Form(...),
    video_title: str = Form(...),
    video_description: str = Form(None),
    chunk_num: int = Form(0),
    total_chunks: int = Form(1),
    chunks: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    base = tempfile.gettempdir()
    dir_path = os.path.join(base, "medieo", up_id)
    file_path = f"{dir_path}/chunk_{chunk_num}"
    assembled_path = os.path.join(dir_path, "assembled.mp4")
    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        print("Error creating temporary chunks folder...")
        return HTTPException(status_code=503, detail="Internal error occured.")

    is_last = chunk_num + 1 == total_chunks
    
    if chunk_num == 0:
        existing = db.query(Video).filter(Video.upload_id == up_id).first()
        if not existing:
            create_video(db, upload_id=up_id, title=video_title, description=video_description)

    with open(file_path, "wb") as bf:
        while content := await chunks.read(1024 * 1024):
            bf.write(content)

    if is_last:
        with open(assembled_path, "wb") as bf:
            chunk = 0
            while chunk < total_chunks:
                chunk_fp = f"{dir_path}/chunk_{chunk}"
                with open(chunk_fp, "rb") as bff:
                    while data := bff.read(1024 * 1024):
                        bf.write(data)
                os.remove(chunk_fp)
                chunk += 1
        task = transcode_t_hls.delay(assembled_path, up_id)
        return JSONResponse(
            {"message": "File uploaded successfully", "task_id": task.id},
            status_code=status.HTTP_201_CREATED,
        )  # type: ignore

    return JSONResponse(
        {"message": "Chunk uploaded successfully"}, status_code=status.HTTP_201_CREATED
    )
