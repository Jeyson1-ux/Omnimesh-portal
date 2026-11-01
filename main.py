import time
from fastapi import FastAPI, Response
from prometheus_client import generate_latest, Histogram, Counter

app = FastAPI(title="Omnimesh portal")

REQUEST_COUNT = Counter(
    "omnimesh_requests_total",
    "Total amount of requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "omnimesh_request_latency_seconds",
    "Counts the time taken to handle a requets in seconds",
    ["endpoint"]
)


@app.get("/")
def read_root():
    start_time = time.time()

    time.sleep(0.05)

    duration = time.time() - start_time

    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()

    REQUEST_LATENCY.labels(endpoint="/").observe(duration)

    return {"message: Welcome to OmniMesh Portal"}


@app.get("/metrics")
def metrics(): 
    return Response(generate_latest(), media_type="text/plain")