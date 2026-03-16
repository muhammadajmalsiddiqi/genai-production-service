from prometheus_client import Counter, Histogram, Summary

# Standard HTTP metrics
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "Latency of HTTP requests in seconds",
    ["endpoint"]
)

# Model specific metrics
MODEL_INFERENCE_TIME = Summary(
    "model_inference_seconds",
    "Time spent in model inference"
)

PREDICTION_COUNTER = Counter(
    "model_predictions_total",
    "Total number of model predictions generated"
)

MODEL_DRIFT_SCORE = Histogram(
    "model_drift_score",
    "Estimated drift score for the model predictions",
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
)
