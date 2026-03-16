import time
import logging
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from prometheus_client import make_asgi_app
from prometheus_metrics import (
    REQUEST_COUNT,
    REQUEST_LATENCY,
    MODEL_INFERENCE_TIME,
    PREDICTION_COUNTER
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="GenAI Production Service",
    description="Production-ready FastAPI service for Generative AI deployment.",
    version="1.0.0"
)

# Add Prometheus metrics asgi app
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

class GenerationRequest(BaseModel):
    prompt: str
    max_tokens: int = 100
    temperature: float = 0.7

class GenerationResponse(BaseModel):
    text: str
    usage: dict

@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.time()
    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    
    response = await call_next(request)
    
    latency = time.time() - start_time
    REQUEST_LATENCY.labels(endpoint=request.url.path).observe(latency)
    
    return response

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/generate", response_model=GenerationResponse)
async def generate_text(request: GenerationRequest):
    logger.info(f"Received generation request: {request.prompt[:50]}...")
    
    inference_start = time.time()
    try:
        # Mock inference logic - replace with actual LLM call
        time.sleep(0.5) # Simulate latency
        generated_text = f"Simulated response for: {request.prompt}"
        
        inference_time = time.time() - inference_start
        MODEL_INFERENCE_TIME.observe(inference_time)
        PREDICTION_COUNTER.inc()
        
        return GenerationResponse(
            text=generated_text,
            usage={"prompt_tokens": len(request.prompt) // 4, "completion_tokens": len(generated_text) // 4}
        )
    except Exception as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Inference engine error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
