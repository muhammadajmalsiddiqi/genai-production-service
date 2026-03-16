from fastapi import FastAPI, Request
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
import time

app = FastAPI()

# Metrics
REQUEST_COUNT = Counter("http_requests_total", "Total HTTP Requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "HTTP Request Latency", ["endpoint"])

@app.middleware("http")
async def add_metrics(request: Request, call_next):
    start_time = time.time()
    endpoint = request.url.path
    REQUEST_COUNT.labels(method=request.method, endpoint=endpoint).inc()
    
    response = await call_next(request)
    
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint=endpoint).observe(latency)
    return response

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

# ... rest of the API logic from previous version
