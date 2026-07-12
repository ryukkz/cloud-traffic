from .registry import SERVICE_REGISTRY
from collections import defaultdict

class RoundRobinLoadBalancer:
    def __init__(self):
        self.counters=defaultdict(int)
    
    def get_instance(self,service_name,instances):
        if not instances:
            return None
        index=self.counters[service_name]%len(instances)
        self.counters[service_name]+=1
        return instances[index]

    def request_started(self, instance):
        pass

    def request_finished(self, instance):
        pass

class LeastConnectionsLoadBalancer:
    def __init__(self):
        self.counter=defaultdict(int)

    def get_instance(self,service_name,instances):
        if not instances:
            return None
        #find all the instances with min connections
        minimum= min(instance.active_connections for instance in instances)
        #if some instances have same minimum no of connections,put them in candidate list and use round robin
        candidates=[instance for instance in instances if instance.active_connections==minimum] 
        index=self.counter[service_name]%len(candidates)
        self.counter[service_name]+=1
        return candidates[index]

    def request_started(self,instance):
        instance.active_connections+=1
    
    def request_finished(self,instance):
        if instance.active_connections>0:
            instance.active_connections-=1


class WeightedRoundRobinLoadBalancer:
    def __init__(self):
        self.counter = defaultdict(int)

    def get_instance(self, service_name, instances):

        if not instances:
            return None

        weighted_instances = []

        for instance in instances:
            weighted_instances.extend([instance] * instance.weight)
        print("\n---------------------")
        print("Counter:", self.counter[service_name])
        print("Weighted List:", [i.url for i in weighted_instances])
        index = self.counter[service_name] % len(weighted_instances)
        selected = weighted_instances[index]
        print("Selected:", selected.url)
        self.counter[service_name] += 1

        return selected
    def request_started(self, instance):
        pass

    def request_finished(self, instance):
        pass