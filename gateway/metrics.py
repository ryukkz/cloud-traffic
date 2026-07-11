from prometheus_client import Counter,Histogram,Gauge

from prometheus_client import Counter, Histogram, Gauge

# Total HTTP requests
REQUEST_COUNT = Counter(
    "gateway_requests_total",
    "Total number of requests",
    ["method", "endpoint", "status"]
)

# Request latency
REQUEST_LATENCY = Histogram(
    "gateway_request_latency_seconds",
    "Request latency",
    ["endpoint"]
)

# Currently alive backend servers
ACTIVE_SERVERS = Gauge(
    "gateway_active_servers",
    "Number of active backend servers"
)

# Active connections
ACTIVE_CONNECTIONS = Gauge(
    "gateway_active_connections",
    "Current active connections"
)

# Circuit breaker state
CIRCUIT_STATE = Gauge(
    "gateway_circuit_state",
    "Circuit state of backend",
    ["server"]
)

# Rate limited requests
RATE_LIMITED = Counter(
    "gateway_rate_limited_total",
    "Requests blocked by rate limiter"
)