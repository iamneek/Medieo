from fastapi import FastAPI, status
from .routes import upload_route, watch_route
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.include_router(upload_route.router)
app.include_router(watch_route.router)
app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_methods=["*"],
                   allow_headers=["*"])

@app.get("/")
def home():
    return JSONResponse({"message": "welcome"}, status_code=status.HTTP_200_OK)