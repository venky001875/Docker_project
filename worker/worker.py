import time
import json
import redis
import os
import sys

# Dynamically find the absolute path to the 'dao' folder relative to this worker.py file
current_dir = os.path.dirname(os.path.abspath(__file__))
dao_path = os.path.join(current_dir, "..", "dao")
sys.path.append(dao_path)

from repository import save_task

# FIX: Added socket_timeout and retry configurations to keep connection alive indefinitely
r = redis.Redis(
    host="localhost", 
    port=6379, 
    decode_responses=True,
    socket_timeout=60,             # Checks connection life every 60 seconds
    socket_connect_timeout=10,
    retry_on_timeout=True          # Automatically reconnects if a timeout occurs
)

print("🚀 Background Worker started... Waiting for tasks in 'task_queue'...")

while True:
    try:
        # BLPOP blocks the script until an item is available in the 'task_queue'
        task_data = r.blpop("task_queue", timeout=0)
        
        if task_data:
            queue_name, message = task_data
            task = json.loads(message)
            
            task_id = task.get("task_id")
            number = task.get("number")
            
            print(f"📦 Processing Task {task_id}: Calculating square of {number}...")
            
            r.set(f"task:{task_id}:status", "processing")
            
            time.sleep(2)  # Simulate heavy processing
            result = number * number
            
            save_task(task_id, number, result)
            
            r.set(f"task:{task_id}:result", result)
            r.set(f"task:{task_id}:status", "completed")
            r.set(f"result:{number}", result, ex=3600)
            
            print(f"✅ Task {task_id} complete! Result {result} cached and saved to DB.")
            
    except redis.exceptions.TimeoutError:
        # If Redis idles too long, it will fire this block, print this message, and loop back smoothly without crashing!
        print("🔄 Connection idled. Refreshing worker connection pool...")
        continue
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        time.sleep(2)