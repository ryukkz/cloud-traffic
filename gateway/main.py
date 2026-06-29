from fastapi import FastAPI,Request,HTTPException
import httpx
from fastapi.responses import Response
from models import ServiceRegistration
from service_registry import ServiceRegistry
from registry import SERVICE_REGISTRY
app=FastAPI()
registry=ServiceRegistry()
@app.get("/")
def home():
    return {
        "message": "Cloud Traffic Manager Gateway"
    }

@app.api_route("/{service}/{path:path}",methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service:str,path:str,request:Request):
    instances=registry.get_instances(service)
    if not instances:
        raise HTTPException(
            status_code=404,
            detail="No instances found"
        )
    instance=instances[0]
    if path:
        url=f"{instance.url}/{service}/{path}"
    else:
        url=f"{instance.url}/{service}"
    body=await request.body()
    headers=dict(request.headers)
    params=request.query_params
    
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

@app.post("/register")
def register(service:ServiceRegistration):
    registry.register(
        service.service,service.url
    )
    
    return {
        "message": "Registered Successfully"
        
    }

@app.get("/registry")
def registry1():
    return registry.get_registry()


@app.post("/unregister")
def unregister(service: ServiceRegistration):

    success = registry.unregister(
        service.service,
        service.url
    )

    if success:
        return {"message": "Service Unregistered"}

    return {"message": "Service Not Found"}