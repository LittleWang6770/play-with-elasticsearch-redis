import redis
from elasticsearch import Elasticsearch

# Redis credentials from your config
REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_USER = "default"  # From REDIS_TASK_USER
REDIS_PASSWORD = "sOmE_sEcUrE_pAsS"  # From REDIS_TASK_PASSWORD
REDIS_DB = 2  # From REDIS_TASK_DB

# Elasticsearch host
ES_HOST = "http://elasticsearch:9200"

# Connect to Redis with authentication
redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    username=REDIS_USER,
    password=REDIS_PASSWORD,
    db=REDIS_DB,
    decode_responses=True
)

# Connect to Elasticsearch
es = Elasticsearch([ES_HOST])

# --- Redis Demo ---
print("\n--- Redis Demo ---")
# Set a key-value pair in Redis
redis_client.set("message", "Hello from Redis with authentication!")
# Retrieve the value
message = redis_client.get("message")
print(f"Redis stored message: {message}")

# --- Elasticsearch Demo ---
print("\n--- Elasticsearch Demo ---")
# Index a simple document
doc = {
    "name": "Alice",
    "age": 30,
    "message": "Hello from Elasticsearch!"
}
es.index(index="demo_index", id=1, document=doc)

# Retrieve the document
retrieved_doc = es.get(index="demo_index", id=1)
print(f"Elasticsearch retrieved document: {retrieved_doc['_source']}")
