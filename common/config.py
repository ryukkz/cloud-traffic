import os

GATEWAY_URL = os.getenv(
    "GATEWAY_URL",
    "http://127.0.0.1:8000"
)

SERVICE_URL = os.getenv(
    "SERVICE_URL",
    "http://127.0.0.1:8002"
)

SERVICE_WEIGHT = int(
    os.getenv("SERVICE_WEIGHT", 1)
)

HEARTBEAT_INTERVAL = int(
    os.getenv("HEARTBEAT_INTERVAL", 5)
)

MAX_RETRIES = int(
    os.getenv("MAX_RETRIES", 2)
)

RETRY_DELAY = float(
    os.getenv("RETRY_DELAY", 0.2)
)