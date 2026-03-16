# GenAI Production Service 🚀🏭

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/Docker-Multi--stage-blue?logo=docker)](https://www.docker.com/)

A production-ready FastAPI service for deploying and monitoring Generative AI models. This repository implements industry-standard MLOps practices, featuring asynchronous task processing, rate limiting, and exhaustive monitoring.

## 🌟 Key Features
- **Asynchronous Processing**: Integrated **Celery & Redis** for handling long-running inference tasks.
- **Rate Limiting**: Built-in protection against API abuse using `SlowAPI`.
- **Advanced Monitoring**: Real-time metrics via **Prometheus** and ready-to-use **Grafana** dashboards.
- **Optimized Docker**: Multi-stage builds for minimal image size and enhanced security.
- **Automated API Docs**: Fully compliant OpenAPI/Swagger documentation.

## 📈 Monitoring & Observability

### Prometheus Metrics
Metrics are exposed at `/metrics`:
- `http_requests_total`: Request count by endpoint.
- `model_inference_seconds`: Latency of the model forward pass.
- `rate_limit_exceeded_total`: Count of blocked requests.

### Grafana Dashboard
A sample dashboard configuration is provided in `monitoring/grafana_dashboard.json`.

## 🛠️ Installation

```bash
git clone https://github.com/dirk-kuijprs/genai-production-service.git
cd genai-production-service
pip install -r requirements.txt celery redis slowapi
```

## 🚀 Running the Service

### Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

### Manual Execution
1. Start Redis: `redis-server`
2. Start Celery: `celery -A main.celery_app worker --loglevel=info`
3. Start FastAPI: `uvicorn main:app --host 0.0.0.0 --port 8000`

## 📡 API Endpoints

| Method | Endpoint | Description | Rate Limit |
|--------|----------|-------------|------------|
| `GET` | `/health` | Service health check | 5/min |
| `POST` | `/generate` | Synchronous text generation | 10/min |
| `POST` | `/generate-async` | Asynchronous task submission | N/A |
| `GET` | `/metrics` | Prometheus metrics | N/A |

## 👨‍💻 Author
**Dirk Kuijprs**  
Data Scientist at G42

Special thanks to **Muhammad Ajmal Siddiqui** for his mentorship and guidance. Connect with him on [LinkedIn](https://www.linkedin.com/in/muhammadajmalsiddiqi/).

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
