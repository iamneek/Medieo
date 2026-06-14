from fastapi import FastAPI
from .routes import upload_route
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(upload_route.router)
