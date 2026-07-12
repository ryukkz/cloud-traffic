from fastapi import APIRouter
from ..analytics import analytics
from ..metrics import RATE_LIMITED
from ..registry import SERVICE_REGISTRY

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/summary")
def summary():
    return {
        "total_requests": analytics.total_requests,
        "average_latency": analytics.average_latency(),
        "active_servers": sum(
            len(v) for v in SERVICE_REGISTRY.values()
        ),
        "rate_limited_requests": RATE_LIMITED._value.get(),
    }


@router.get("/endpoints")
def endpoints():
    return analytics.endpoint_requests


@router.get("/backends")
def backends():
    return analytics.backend_requests


@router.get("/errors")
def errors():
    return analytics.status_codes