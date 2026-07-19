# Cloud Traffic Manager

A scalable **API Gateway and Traffic Management System** built using **FastAPI**, designed to efficiently route requests across multiple microservices. The project implements service discovery, multiple load balancing strategies, health monitoring, circuit breaking, Redis-based rate limiting, and real-time observability using Prometheus and Grafana.

---

## Features

- API Gateway for centralized request routing
- Service Discovery with automatic registration and deregistration
- Heartbeat-based Health Monitoring
- Multiple Load Balancing Algorithms
  - Round Robin
  - Least Connections
  - Weighted Round Robin
- Circuit Breaker for fault tolerance
- Redis-based Rate Limiting
- Request Retry Mechanism
- Prometheus Metrics Collection
- Grafana Monitoring Dashboard
- Dockerized Microservices Architecture
- Locust-based Load Testing

---

## Architecture

```
                        Client
                           │
                           ▼
                    API Gateway (FastAPI)
                           │
        ┌──────────────────┼──────────────────┐
        ▼                  ▼                  ▼
  User Service      Product Service     Order Service
        │                  │                  │
        └──────────────┬───┴──────────────────┘
                       ▼
                  Service Registry
                       │
        Heartbeat & Health Monitoring
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
      Redis                     Prometheus
 (Rate Limiting)             (Metrics Collection)
                                   │
                                   ▼
                              Grafana Dashboard
```

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Backend | FastAPI, Python |
| Reverse Proxy | API Gateway |
| Database | In-Memory Service Registry |
| Cache | Redis |
| Monitoring | Prometheus, Grafana |
| Load Testing | Locust |
| Containerization | Docker, Docker Compose |
| HTTP Client | HTTPX |
| Metrics | prometheus_client |

---

## Load Balancing Algorithms

### Round Robin

Routes requests sequentially across all healthy service instances.

Example:

```
Request 1 → User Service 1

Request 2 → User Service 2

Request 3 → User Service 3

Request 4 → User Service 1
```

---

### Least Connections

Routes incoming requests to the instance with the fewest active connections.

Suitable for uneven workloads.

---

### Weighted Round Robin

Distributes traffic based on server weights.

Example:

```
Server A (Weight = 3)

Server B (Weight = 1)

Traffic Distribution

A
A
A
B
A
A
A
B
```

---

## Health Monitoring

Every microservice periodically sends heartbeat messages to the API Gateway.

If a heartbeat is not received within the configured timeout:

- Service is marked unhealthy
- Removed from load balancing
- Requests are redirected to healthy instances

---

## Circuit Breaker

To prevent cascading failures:

- Tracks failed requests
- Opens the circuit after repeated failures
- Temporarily blocks requests to unhealthy services
- Automatically retries after the recovery timeout

---

## Rate Limiting

Implemented using Redis.

Each client IP has:

- Configurable request limit
- Configurable time window

When exceeded:

```
HTTP 429 Too Many Requests
```

is returned immediately.

---

## Monitoring

Prometheus continuously collects metrics from the gateway.

Collected metrics include:

- Total Requests
- Request Latency
- Active Connections
- Active Servers
- HTTP Status Codes
- Rate Limited Requests

Grafana visualizes these metrics in real time.

---

## Project Structure

```
CloudTrafficManager/

│
├── gateway/
│   ├── load_balancer/
│   ├── registry/
│   ├── monitoring/
│   ├── middleware/
│   ├── routes/
│   └── main.py
│
├── services/
│   ├── userService/
│   ├── productService/
│   └── orderService/
│
├── common/
│
├── prometheus/
│
├── grafana/
│
├── docker-compose.yml
│
└── README.md
```

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/cloud-traffic-manager.git

cd cloud-traffic-manager
```

---

### Start the Project

```bash
docker compose up -d --build
```

---

### Verify Running Containers

```bash
docker compose ps
```

---

## Access the Services

| Service | URL |
|----------|-----|
| API Gateway | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 |
| Locust | http://localhost:8089 |

---

## Demonstration Workflow

### Step 1

Start all containers.

```bash
docker compose up -d --build
```

---

### Step 2

Open Swagger UI.

```
http://localhost:8000/docs
```

Test available endpoints.

---

### Step 3

Open Grafana.

```
http://localhost:3000
```

Observe:

- Request Throughput
- Active Servers
- Active Connections
- Request Latency
- Rate Limited Requests

---

### Step 4

Open Locust.

```
http://localhost:8089
```

Configure:

```
Host

http://localhost:8000

Users

50

Spawn Rate

5
```

Start swarming.

---

### Step 5

Return to Grafana.

Observe metrics updating in real time.

---

## Performance Testing

Load testing is performed using Locust to simulate concurrent users and evaluate:

- Request throughput
- Average latency
- Gateway scalability
- Load balancing effectiveness
- Fault tolerance

---

## Future Enhancements

- JWT Authentication
- Dynamic Service Scaling
- Kubernetes Deployment
- Distributed Service Registry
- Database-backed Service Registry
- Request Analytics Dashboard
- Role-Based Access Control
- gRPC Service Support
- Distributed Tracing using Jaeger

---

## Learning Outcomes

This project demonstrates practical implementation of:

- API Gateway Design
- Microservices Architecture
- Reverse Proxying
- Service Discovery
- Load Balancing Algorithms
- Distributed Systems Concepts
- Fault Tolerance
- Rate Limiting
- Monitoring & Observability
- Docker-based Deployment
- Performance Testing

---

## Screenshots

<img width="1762" height="741" alt="image" src="https://github.com/user-attachments/assets/f8c6ec0c-bda6-4975-a0b8-d7e30bea5bac" />
<img width="1903" height="587" alt="image" src="https://github.com/user-attachments/assets/cb7d81c1-686c-46d4-960b-a3c567ef8ca9" />


---

## Author

**Geethanjali S**

B.Tech Computer Science Engineering

Backend | Distributed Systems | FastAPI | Docker | Microservices
