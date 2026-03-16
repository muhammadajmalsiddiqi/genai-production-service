# GenAI Production Service 🚀🏭

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg)](https://fastapi.tiangolo.com/)

A production-ready FastAPI service for deploying and monitoring Generative AI models. This repository implements best practices for MLOps, including structured logging, health checks, and real-time monitoring with Prometheus.

## 🌟 Key Features
- **High Performance**: Built on FastAPI and Uvicorn for asynchronous, high-throughput inference.
- **MLOps Monitoring**: Integrated Prometheus metrics for tracking latency, throughput, and model-specific performance.
- **Production-Grade**: Multi-stage Docker builds optimized for size and security.
- **Robust Error Handling**: Standardized API responses and comprehensive middleware for request tracking.
- **Scalable Architecture**: Designed to be deployed behind a load balancer (e.g., Nginx, Traefik) or within a Kubernetes cluster.

## 🛠️ Installation

```bash
git clone https://github.com/dirk-kuijprs/genai-production-service.git
cd genai-production-service
pip install -r requirements.txt
```

## 🚀 Running with Docker

```bash
docker build -t genai-service .
docker run -p 8000:8000 genai-service
```

Access the API documentation at `http://localhost:8000/docs`.

## 📈 Monitoring
Metrics are exposed at the `/metrics` endpoint for Prometheus scraping.
- `http_requests_total`: Total number of requests by method and endpoint.
- `model_inference_seconds`: Time spent in the model's forward pass.
- `model_predictions_total`: Total count of predictions served.

## 👨‍💻 Author
**Dirk Kuijprs**  
Data Scientist at G42

Special thanks to **Muhammad Ajmal Siddiqui** for his mentorship and guidance. Connect with him on [LinkedIn](https://www.linkedin.com/in/muhammadajmalsiddiqi/).

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
