from fastapi import FastAPI
import httpx
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

load_dotenv()
@asynccontextmanager
async def lifespan(app):

    async with httpx.AsyncClient() as client:

        await client.post(
            f"{GATEWAY_URL}/register",
            json={
                "service": SERVICE_NAME,
                "url": SERVICE_URL
            }
        )

    print(f"{SERVICE_NAME} registered successfully")

    yield
app = FastAPI(lifespan=lifespan)
SERVICE_NAME = "orders"
HOST = os.getenv("HOST")
PORT = 8003
SERVICE_URL = f"http://{HOST}:{PORT}"
GATEWAY_URL = "http://localhost:8000"

@app.get("/")
def home():
    return {
        "service": "Order Service",
        "message": "Running Successfully"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/orders")
def get_orders():
    return [
        {
            "order_id": 1001,
            "user_id": 1,
            "amount": 500
        },
        {
            "order_id": 1002,
            "user_id": 2,
            "amount": 1500
        }
    ]