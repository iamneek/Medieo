from fastapi import FastAPI, status, Depends
from .routes import upload_route, watch_route
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .repo import video_repo
from .database import get_db
from sqlalchemy.orm import Session

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.include_router(upload_route.router)
app.include_router(watch_route.router)
app.add_middleware(
    CORSMiddleware, allow_origins=origins, allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def home(db: Session = Depends(get_db), page: int = 1, limit: int = 10):
    return video_repo.get_all_videos(db=db, page=page, limit=limit)
