import time
import logging
import uuid
import json
from fastapi import FastAPI, Request, Response
from routes import ProcessRequest
from cache import redis_client

# Configure professional, structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("api-gateway")

app = FastAPI(
    title="Python Microservices Pipeline",
    version="1.0.0",
    description="FastAPI Gateway with Redis Caching"
)

# ⏱️ STEP 4: Request Timing Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    
    # Logs every request, method, path, and its exact processing speed
    logger.info(
        f"METHOD: {request.method} | PATH: {request.url.path} | "
        f"LATENCY: {process_time:.4f}s | STATUS: {response.status_code}"
    )
    
    return response

@app.get("/")
def root():
    return {
        "message": "FastAPI Gateway Running"
    }

# 🩺 STEP 1: Upgraded Health Check (Docker uses this)
@app.get("/health")
def health():
    try:
        redis_client.ping()
        return {
            "status": "healthy",
            "redis": "connected"
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "redis": "disconnected"
        }

# 📈 STEP 3: Upgraded Prometheus Metrics Endpoint (Plain Text Format)
@app.get("/metrics")
def metrics():
    try:
        keys = redis_client.keys("*")
        total_keys = len(keys)
        status_val = 1  # 1 means healthy/running
    except Exception:
        total_keys = -1  # Indicates redis is down to monitoring tools
        status_val = 0   # 0 means degraded

    # Format the response exactly how Prometheus needs it (Plain text lines)
    metrics_output = (
        "# HELP api_gateway_status Current status of the API Gateway (1 for running)\n"
        "# TYPE api_gateway_status gauge\n"
        f"api_gateway_status {status_val}\n\n"
        "# HELP redis_total_keys Total number of active keys cached in Redis\n"
        "# TYPE redis_total_keys gauge\n"
        f"redis_total_keys {total_keys}\n"
    )
    
    # media_type="text/plain" strips away JSON formatting headers
    return Response(content=metrics_output, media_type="text/plain")

@app.post("/process")
def process(data: ProcessRequest):
    cache_key = f"result:{data.number}"
    cached_result = redis_client.get(cache_key)

    if cached_result:
        logger.info(f"Cache HIT for number: {data.number}")
        return {
            "source": "cache",
            "result": int(cached_result)
        }

    logger.info(f"Cache MISS for number: {data.number}. Generating task...")
    task_id = str(uuid.uuid4())
    task_data = {
        "task_id": task_id,
        "number": data.number
    }

    redis_client.rpush(
        "task_queue",
        json.dumps(task_data)
    )

    return {
        "task_id": task_id,
        "status": "queued"
    }

@app.get("/result/{task_id}")
def get_result(task_id: str):
    result = redis_client.get(f"task:{task_id}")

    if result:
        return {
            "status": "completed",
            "result": json.loads(result)
        }

    return {
        "status": "processing"
    }

@app.get("/cache/stats")
def cache_stats():
    keys = redis_client.keys("*")
    return {
        "total_keys": len(keys),
        "keys": keys
    }