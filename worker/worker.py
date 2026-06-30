import time
import json
import redis
import os
import sys
import logging

# Configure professional, structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger("background-worker")

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

r = redis.Redis(
    host="redis", 
    port=6379, 
    decode_responses=True,
    socket_timeout=60,             
    socket_connect_timeout=10,
    retry_on_timeout=True          
)

logger.info("🚀 Background Worker started... Waiting for tasks in 'task_queue'...")

while True:
    try:
        task_data = r.blpop("task_queue", timeout=0)
        
        if task_data:
            queue_name, message = task_data
            task = json.loads(message)
            
            task_id = task.get("task_id")
            number = task.get("number")
            
            logger.info(f"📦 TASK RECEIVED | task_id: {task_id} | Calculating square of {number}...")
            
            time.sleep(2)  # Simulating heavy background processing
            result = number * number
            
            response_payload = {
                "result": result
            }
            r.set(f"task:{task_id}", json.dumps(response_payload))
            r.set(f"result:{number}", result, ex=3600)
            
            logger.info(f"✅ TASK COMPLETE | task_id: {task_id} | Result {result} cached successfully.")
            
    except redis.exceptions.TimeoutError:
        logger.warning("🔄 Connection idled. Refreshing worker connection pool...")
        continue
    except Exception as e:
        logger.error(f"❌ Unexpected Error: {str(e)}")
        time.sleep(2)