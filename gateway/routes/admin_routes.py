from fastapi import APIRouter
from ..state import registry, circuit_breakers
from pydantic import BaseModel

class ServerControl(BaseModel):
    service:str
    url:str


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.get("/servers")
def servers():

    result = []

    for service, instances in registry.get_registry().items():

        for instance in instances:

            result.append({
                "service": service,
                "url": instance.url,
                "healthy": instance.healthy,
                "weight": instance.weight,
                "active_connections": instance.active_connections,
                "circuit_open": not circuit_breakers[instance.url].allow_request()
            })

    return result


@router.post("/disable")
def disable(server:ServerControl):

    instances = registry.get_registry().get(server.service)
    if not instances:
        return {
            "message": f"Service '{server.service}' not found"
        }

    for instance in instances:

        if instance.url == server.url:
            instance.healthy = False
            return {
                "message": "Server disabled"
            }

    return {
        "message": "Server not found"
    }

@router.post("/enable")
def enable(server:ServerControl):
    instances = registry.get_registry().get(server.service)
    if not instances:
        return {
            "message": f"Service '{server.service}' not found"
        }
    for instance in instances:

        if instance.url==server.url:

            instance.healthy=True

            return {
                "message":"Server enabled"
            }

    return {
        "message":"Server not found"
    }

@router.get("/health")
def gateway_health():

    total = 0
    healthy = 0

    for instances in registry.get_registry().values():

        for instance in instances:

            total += 1

            if instance.healthy:
                healthy += 1

    return {

        "gateway":"Healthy",

        "healthy_servers":healthy,

        "total_servers":total
    }