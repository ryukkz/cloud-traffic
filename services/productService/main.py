from fastapi import FastAPI

import httpx
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv
from routes import router

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
    async with httpx.AsyncClient() as client:

        await client.post(
            f"{GATEWAY_URL}/unregister",
            json={
                "service": SERVICE_NAME,
                "url": SERVICE_URL
            }
        )

    print("Unregistered")
app = FastAPI(lifespan=lifespan)
app.include_router(router)
SERVICE_NAME = "products"
HOST = os.getenv("HOST")
PORT = 8002
SERVICE_URL = f"http://{HOST}:{PORT}"
GATEWAY_URL = "http://localhost:8000"



@app.get("/")
def home():
    return {
        "service": "Product Service",
        "message": "Running Successfully"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}



