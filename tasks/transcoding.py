from celery_app import app
from storage.s3 import s3_transcoded_upload
import os
import tempfile
import subprocess


BASE_DIR = tempfile.gettempdir()

def run_ffmpeg(file_path: str, playlist_path: str):
    cmd = [
        "ffmpeg", "-i", file_path,
        "-codec:v", "copy",
        "-codec:a", "copy",
        "-start_number", "0",
        "-hls_time", "10",
        "-hls_list_size", "0",
        "-f", "hls",
        playlist_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr}")
    
@app.task
def transcode_t_hls(file_path, upload_id):
    dir_path = os.path.join(BASE_DIR, "medieo", upload_id, "hls")
    playlist_path = os.path.join(dir_path, "index.m3u8")
    os.makedirs(dir_path, exist_ok=True)
    run_ffmpeg(file_path, playlist_path)
    print(f"File exists: {os.path.exists(file_path)}")
    print(f"File size: {os.path.getsize(file_path)}")
    print(f"File path: {file_path}")
    for filename in os.listdir(dir_path):
        s3_transcoded_upload(os.path.join(dir_path, filename), f"videos/{upload_id}/{filename}")
    return "Transcoding successful"