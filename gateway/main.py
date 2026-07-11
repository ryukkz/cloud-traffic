from fastapi import FastAPI,Request,HTTPException
import httpx
from fastapi.responses import Response
from models import ServiceRegistration
from service_registry import ServiceRegistry
import asyncio
from contextlib import asynccontextmanager
from registry import SERVICE_REGISTRY
from load_balancer import RoundRobinLoadBalancer,LeastConnectionsLoadBalancer,WeightedRoundRobinLoadBalancer
from circuit_breaker import CircuitBreaker
from rate_limiter import RateLimiter
from prometheus_client import make_asgi_app
import time 
from metrics import ( REQUEST_COUNT,
    REQUEST_LATENCY,
    ACTIVE_CONNECTIONS,
    ACTIVE_SERVERS,
    CIRCUIT_STATE,
    RATE_LIMITED)

load_balancer=WeightedRoundRobinLoadBalancer()
circuit_breakers={}
rate_limiter=RateLimiter()

@asynccontextmanager
async def lifespan(app):
    task = asyncio.create_task(cleanup_task())
    yield
    task.cancel()


app=FastAPI(lifespan=lifespan)
registry=ServiceRegistry()
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
@app.get("/")
def home():
    return {
        "message": "Cloud Traffic Manager Gateway"
    }

@app.api_route("/{service}/{path:path}",methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def gateway(service:str,path:str,request:Request):
    client_ip = request.client.host

    if not rate_limiter.allow_request(client_ip):
        RATE_LIMITED.inc()

        raise HTTPException(
            status_code=429,
            detail="Too Many Requests"
        )
    instances=registry.get_instances(service)
    healthy_instances = [instance for instance in instances if instance.healthy and circuit_breakers[instance.url].allow_request()]
    if not healthy_instances:
        raise HTTPException(
            status_code=503,
            detail="No healthy instances found"
        )
    instance=load_balancer.get_instance(service, healthy_instances)
    load_balancer.request_started(instance)
    if path:
        url=f"{instance.url}/{service}/{path}"
    else:
        url=f"{instance.url}/{service}"
    body=await request.body()
    headers=dict(request.headers)
    params=request.query_params
    print(f"[Gateway] Forwarding {service} request to {instance.url}")
    start = time.time()
    status = 500
    ACTIVE_CONNECTIONS.inc()
    try:
        async with httpx.AsyncClient() as client:
            response=await client.request(
                method=request.method,
                url=url,
                content=body,
                headers=headers,
                params=params
            )
        status = response.status_code
        circuit_breakers[instance.url].record_success()
        return Response(
        content=response.content,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.headers.get("content-type")
    )
    except Exception:
        status=503
        circuit_breakers[instance.url].record_failure()

        raise HTTPException(
        status_code=503,
        detail="Backend service unavailable"
        )
    finally:
        duration = time.time() - start

        REQUEST_COUNT.labels(
            request.method,
            request.url.path,
            str(status)
        ).inc()

        REQUEST_LATENCY.labels(
            request.url.path
        ).observe(duration)

        ACTIVE_CONNECTIONS.dec()

        load_balancer.request_finished(instance)

@app.post("/register")
def register(service:ServiceRegistration):
    registry.register(
        service.service,service.url,service.weight
    )
    ACTIVE_SERVERS.set(
        sum(len(v) for v in registry.get_registry().values())
    )
    if service.url not in circuit_breakers:
        circuit_breakers[service.url] = CircuitBreaker()
        CIRCUIT_STATE.labels(service.url).set(0)
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
        ACTIVE_SERVERS.set(
            sum(len(v) for v in registry.get_registry().values())
        )
        return {"message": "Service Unregistered"}

    return {"message": "Service Not Found"}

@app.post("/heartbeat")
def heartbeat(service:ServiceRegistration):
    print("Heartbeat received:", service.service, service.url)

    success=registry.heartbeat(service.service,service.url)
    if success:
        return {"message":"Heartbeat updated"}
    return {"message":"Service Not registered"}

async def cleanup_task():
    while True:
        registry.cleanup()
        await asyncio.sleep(5)