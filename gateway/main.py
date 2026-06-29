from fastapi import FastAPI
import httpx
from config import SERVICE_MAP
app=FastAPI()

@app.get("/")
def home():
    return {
        "message": "Cloud Traffic Manager Gateway"
    }

@app.api_route("/{service}",methods=["GET"])
async def gateway(service:str):
    if service not in SERVICE_MAP:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )
    url=f"{SERVICE_MAP[service]}/{service}"
    async with httpx.AsyncClient() as client:
        response=await client.get(url)
        return response.json()