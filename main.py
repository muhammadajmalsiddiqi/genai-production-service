import time
import logging
from fastapi import FastAPI, HTTPException, Request, Depends
from pydantic import BaseModel
from prometheus_client import make_asgi_app
from prometheus_metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    MODEL_INFERENCE_TIME,
    PREDICTION_COUNTER
)
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from celery import Celery

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Rate Limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize Celery for Async Tasks
celery_app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

app = FastAPI(
    title="GenAI Production Service",
    description="Production-ready FastAPI service with Async Processing, Rate Limiting, and Monitoring.",
    version="1.1.0"
)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add Prometheus metrics asgi app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class GenerationResponse(BaseModel):
    task_id: str = None
    text: str = None
    usage: dict = None

@celery_app.task(name="tasks.generate_text_async")
def generate_text_async(prompt: str):
    # Long-running inference logic
    time.sleep(2)
    return f"Processed: {prompt}"

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    
    response = await call_next(request)
    
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)
    
    return response

@app.get("/health")
@limiter.limit("5/minute")
async def health_check(request: Request):
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "services": {
            "api": "up",
            "redis": "connected",
            "celery_workers": "active"
        }
    }

@app.post("/generate", response_model=GenerationResponse)
@limiter.limit("10/minute")
async def generate_text(request: Request, gen_request: GenerationRequest):
    logger.info(f"Received generation request: {gen_request.prompt[:50]}...")
    
    inference_start = time.time()
    try:
        # Synchronous inference (standard)
        time.sleep(0.5)
        generated_text = f"Simulated response for: {gen_request.prompt}"
        
        inference_time = time.time() - inference_start
        MODEL_INFERENCE_TIME.observe(inference_time)
        PREDICTION_COUNTER.inc()
        
        return GenerationResponse(
            text=generated_text,
            usage={"prompt_tokens": len(gen_request.prompt) // 4, "completion_tokens": len(generated_text) // 4}
        )
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Inference engine error")

@app.post("/generate-async", response_model=GenerationResponse)
async def generate_text_async_endpoint(request: GenerationRequest):
    task = generate_text_async.delay(request.prompt)
    return GenerationResponse(task_id=task.id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
