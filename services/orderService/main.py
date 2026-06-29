from fastapi import FastAPI 
from common.service_client import create_lifespan
from .routes import router




SERVICE_NAME = "orders"
HOST = "127.0.0.1"
PORT = 8003
SERVICE_URL = f"http://{HOST}:{PORT}"

app = FastAPI(lifespan=create_lifespan(
        SERVICE_NAME,
        SERVICE_URL
    ))

app.include_router(router)
@app.get("/")
def home():
    return {
        "service": "Order Service",
        "message": "Running Successfully"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


