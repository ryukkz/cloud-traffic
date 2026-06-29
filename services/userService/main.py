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
SERVICE_NAME = "users"
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
SERVICE_URL = f"http://{HOST}:{PORT}"
GATEWAY_URL = "http://localhost:8000"

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

@app.get("/users")
def get_users():
    return [
        {
            "id": 1,
            "name": "Alice"
        },
        {
            "id": 2,
            "name": "Bob"
        }
    ]

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "id": user_id,
        "name": f"User {user_id}"
    }


@app.post("/users/login")
def login():
    return {
        "message": "Login Successful"
    }



