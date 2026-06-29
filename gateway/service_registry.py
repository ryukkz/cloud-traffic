from registry import SERVICE_REGISTRY
from datetime import datetime
from models import ServiceInstance
class ServiceRegistry:

    def register(self,service:str,url:str):
        print("Register called")
        if service not in SERVICE_REGISTRY:
            SERVICE_REGISTRY[service] = []
        for instance in SERVICE_REGISTRY[service]:
            if instance.url == url:
                return False
        
        instance = ServiceInstance(
            url=url,
            last_heartbeat=datetime.utcnow()
)
        SERVICE_REGISTRY[service].append(instance)
        return True
    
    
    
    
    def get_instances(self,service:str):
        return SERVICE_REGISTRY.get(service,[])
    def get_registry(self):
        return SERVICE_REGISTRY