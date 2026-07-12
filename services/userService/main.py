from fastapi import FastAPI 
from common.service_client import create_lifespan
from .routes import router
from common.config import SERVICE_URL



SERVICE_NAME = "users"


app = FastAPI(lifespan=create_lifespan(
        SERVICE_NAME,
        SERVICE_URL
    ))

app.include_router(router)
@app.get("/")
def home():
    return {
        "service":"user service",
        "message":"Running successfully"
    }

@app.get("/health")
def health():
    return{
        "status":"healthy"
    }










