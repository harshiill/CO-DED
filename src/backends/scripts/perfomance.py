import time
import logging
from prometheus_client import Counter, Histogram

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics definitions
REQUEST_COUNT = Counter("api_requests_total", "Total API requests", ["endpoint"])
REQUEST_LATENCY = Histogram("api_request_latency_seconds", "Latency for API requests", ["endpoint"])

def record_api_metrics(endpoint: str, func):
    """
    Decorator that records the number of calls and latency for a given endpoint function.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        elapsed_time = time.time() - start_time

        REQUEST_COUNT.labels(endpoint=endpoint).inc()
        REQUEST_LATENCY.labels(endpoint=endpoint).observe(elapsed_time)
        logger.info(f"Endpoint '{endpoint}' executed in {elapsed_time:.3f} seconds")
        return result
    return wrapper

def monitor_api() -> dict:
    """
    Generate a simple performance report. 
    In a production system, you might query Prometheus or a monitoring dashboard.
    """
    # Note: Directly accessing internal metric values (like _sum and _value) is not recommended in production.
    total_requests = sum([REQUEST_COUNT.labels(l)._value.get() for l in REQUEST_COUNT._labelnames])
    total_latency = sum([REQUEST_LATENCY.labels(l)._sum.get() for l in REQUEST_LATENCY._labelnames])

    average_latency = (total_latency / total_requests) if total_requests > 0 else 0

    performance_report = {
        "total_requests": total_requests,
        "average_latency_seconds": average_latency,
    }
    logger.info("Performance Report: %s", performance_report)
    return performance_report

def log_performance(data: dict) -> None:
    """
    Logs the performance data.
    """
    logger.info("Performance Data: %s", data)
