from fastapi import APIRouter, UploadFile, File, Form, status
import uuid
from fastapi.responses import JSONResponse
import os
import tempfile

router = APIRouter()


@router.post("/upload/init")
async def upload_init():
    up_id = str(uuid.uuid4())
    return JSONResponse({"upload_id": up_id}, status_code=status.HTTP_201_CREATED)


@router.post("/upload/")
async def upload_video(
    up_id: str = Form(...),
    chunk_num: int = Form(0),
    total_chunks: int = Form(1),
    chunks: UploadFile = File(...),
):
    base = tempfile.gettempdir()
    dir_path = os.path.join(base, "medieo", up_id)
    file_path = f"{dir_path}/chunk_{chunk_num}"
    assembled_path = os.path.join(dir_path, "assembled")
    try:
        os.makedirs(dir_path, exist_ok=True)
    except Exception as e:
        print("Error creating temporary chunks folder...")
        return status.HTTP_503_SERVICE_UNAVAILABLE

    is_last = chunk_num + 1 == total_chunks
    
    with open(file_path, 'wb') as bf:
        while content := await chunks.read(1024 * 1024):
            bf.write(content)

    if is_last:
        with open(assembled_path, "wb") as bf:
            chunk = 0
            while chunk < total_chunks:
                chunk_fp = f"{dir_path}/chunk_{chunk}"
                with open(chunk_fp, "rb") as bff:
                    while data:= bff.read(1024*1024):
                        bf.write(data)
                os.remove(chunk_fp)
                chunk += 1
        return JSONResponse({"message": "File uploaded successfully"}, status_code = status.HTTP_201_CREATED)
    return JSONResponse({"message": "Chunk uploaded successfully"}, status_code = status.HTTP_201_CREATED)

