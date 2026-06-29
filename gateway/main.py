from fastapi import FastAPI
import httpx
from config import SERVICE_MAP
from fastapi.responses import Response
app=FastAPI()

@app.get("/")
def home():
    return {
        "message": "Cloud Traffic Manager Gateway"
    }

@app.api_route("/{service}/{path:path}",methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service:str,path:str,request:Request):
    if service not in SERVICE_MAP:
        raise HTTPException(
            status_code=404,
            detail="Service not found"
        )
    body=await request.body()
    headers=dict(request.headers)
    params=request.query_params
    url=f"{SERVICE_MAP[service]}/{service}/{path}"
    async with httpx.AsyncClient() as client:
        response=await client.request(
            method=request.method,
            url=url,
            content=body,
            headers=headers,
            params=params
        )
        return Response(
    content=response.content,
    status_code=response.status_code,
    headers=dict(response.headers),
    media_type=response.headers.get("content-type")
)