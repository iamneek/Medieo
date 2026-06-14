from fastapi import FastAPI, status
from .routes import upload_route
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI()
app.include_router(upload_route.router)

@app.get("/")
def home():
    return JSONResponse({"message": "welcome"}, status_code=status.HTTP_200_OK)