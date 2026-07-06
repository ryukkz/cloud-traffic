from registry import SERVICE_REGISTRY
from datetime import datetime,timedelta
from models import ServiceInstance
class ServiceRegistry:

    def register(self,service:str,url:str, weight: int = 1):
        print("Register called")
        if service not in SERVICE_REGISTRY:
            SERVICE_REGISTRY[service] = []
        for instance in SERVICE_REGISTRY[service]:
            if instance.url == url:
                return False
        
        instance = ServiceInstance(
            url=url,
            weight=weight,
            last_heartbeat=datetime.utcnow()
)
        SERVICE_REGISTRY[service].append(instance)
        return True
    
    
    
    
    def get_instances(self,service:str):
        return SERVICE_REGISTRY.get(service,[])
    def get_registry(self):
        return SERVICE_REGISTRY


    def unregister(self, service: str, url: str):
        if service not in SERVICE_REGISTRY:
            return False

        SERVICE_REGISTRY[service] = [
            instance
            for instance in SERVICE_REGISTRY[service]
            if instance.url != url
        ]

        if len(SERVICE_REGISTRY[service]) == 0:
            del SERVICE_REGISTRY[service]

        return True

    def heartbeat(self,service:str,url:str):
        print("Updating heartbeat")
        if service not in SERVICE_REGISTRY:
            return False
        for instance in SERVICE_REGISTRY[service]:
            if instance.url==url:
                instance.last_heartbeat=datetime.utcnow()
                return True
        return False


    def cleanup(self):
        timeout = timedelta(seconds=10)
        now = datetime.utcnow()

        for service in SERVICE_REGISTRY.values():
            for instance in service:
                if now - instance.last_heartbeat > timeout:
                    instance.healthy = False
                else:
                    instance.healthy = True