from pydantic import BaseModel
from datetime import datetime

class ServiceRegistration(BaseModel):
    service: str
    url: str 

class ServiceInstance(BaseModel):

    url: str

    healthy: bool = True

    weight: int = 1

    active_connections: int = 0

    last_heartbeat: datetime

    circuit_state: str = "closed"

# to ensure this format {
#    "service":"users",
#    "url":"http://localhost:8001"
# }