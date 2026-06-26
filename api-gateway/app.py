from fastapi import FastAPI
from routes import ProcessRequest
from cache import redis_client

import uuid
import json

app = FastAPI(
    title="Python Microservices Pipeline",
    version="1.0.0",
    description="FastAPI Gateway with Redis Caching"
)


@app.get("/")
def root():
    return {
        "message": "FastAPI Gateway Running"
    }


@app.get("/health")
def health():

    try:
        redis_client.ping()

        return {
            "status": "healthy",
            "redis": "connected"
        }

    except Exception:

        return {
            "status": "unhealthy",
            "redis": "disconnected"
        }


@app.post("/process")
def process(data: ProcessRequest):

    cache_key = f"result:{data.number}"

    cached_result = redis_client.get(cache_key)

    if cached_result:

        return {
            "source": "cache",
            "result": int(cached_result)
        }

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