from collections import defaultdict

class Analytics:

    def __init__(self):
        self.total_requests = 0
        self.endpoint_requests = defaultdict(int)
        self.status_codes = defaultdict(int)
        self.backend_requests = defaultdict(int)
        self.total_latency = 0.0

    def record_request(self, endpoint, status, backend, latency):
        self.total_requests += 1
        self.endpoint_requests[endpoint] += 1
        self.status_codes[str(status)] += 1
        self.backend_requests[backend] += 1
        self.total_latency += latency

    def average_latency(self):
        if self.total_requests == 0:
            return 0
        return self.total_latency / self.total_requests


analytics = Analytics()