from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import asyncio
import time

app = FastAPI(title="GenAI Production Service", version="1.0.0")

class InferenceRequest(BaseModel):
    prompt: str
    max_tokens: int = 100

class InferenceResponse(BaseModel):
    generated_text: str
    latency_ms: float

@app.get("/")
async def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/generate", response_model=InferenceResponse)
async def generate_text(request: InferenceRequest):
    """High-performance async inference endpoint."""
    start_time = time.time()
    
    # Simulate async model inference with request batching potential
    await asyncio.sleep(0.1) 
    
    latency = (time.time() - start_time) * 1000
    return InferenceResponse(
        generated_text=f"AI response to: {request.prompt}",
        latency_ms=latency
    )

if __name__ == "__main__":
    print("GenAI Production Service starting on http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
