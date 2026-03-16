# GenAI Production Service 🚀🌩️

Highly scalable, enterprise-ready microservice for serving Generative AI models at scale with high concurrency.

## 🌟 Key Capabilities
- **FastAPI Core**: Optimized for low-latency async inference.
- **Request Batching**: Ready for integration with high-performance inference engines.
- **Health Monitoring**: Built-in endpoints for service reliability checks.

## 🛠️ Installation
```bash
git clone https://github.com/vishalmandaki/genai-production-service.git
cd genai-production-service
pip install -r requirements.txt
```

## 🚀 Deployment
```bash
uvicorn src.inference_api:app --host 0.0.0.0 --port 8000
```
Access the interactive API docs at `http://localhost:8000/docs`.
