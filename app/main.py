import redis
from elasticsearch import Elasticsearch
import hashlib
import json

def get_redis_client() -> redis.Redis:
    return redis.Redis(
        host="redis",
        port=6379,
        username="default",
        password="sOmE_sEcUrE_pAsS",
        db=0,
    )

def get_es_client() -> Elasticsearch:
    return Elasticsearch(
        hosts=["http://elasticsearch:9200"])

def generate_unique_cache_id(query: str) -> str:
    """Generate a unique cache ID based on the query."""
    return hashlib.sha256(query.encode()).hexdigest()

def tokenize_query(query: str) -> list:
    """Simple tokenizer to split the query into tokens."""
    return query.split()

def find_cache_id(query: str, es_client: Elasticsearch) -> str:
    """Search for the cache ID in Elasticsearch based on the query."""
    search_body = {
        "query": {
            "match": {
                "query": query
            }
        }
    }
    response = es_client.search(index="query_labels", body=search_body)
    hits = response.get("hits", {}).get("hits", [])
    return hits[0]["_source"].get("cache_id") if hits else None

def generate_response_with_rag(query: str) -> str:
    """Fallback response generation logic (dummy implementation)."""
    return f"Generated response for query: {query}"

def process_query(query: str):
    """Process a query using Redis for caching and Elasticsearch for indexing."""
    redis_client = get_redis_client()
    es_client = get_es_client()

    # Step 1: Find cache_id from Elasticsearch
    cache_id = find_cache_id(query, es_client)
    if cache_id:
        # Step 2: Check Redis for the cached response
        redis_key = f"cache:{cache_id}"
        cached_response = redis_client.get(redis_key)
        if cached_response:
            return json.loads(cached_response)

    # Step 3: Fallback to Response-Augmented Generation (RAG)
    response = generate_response_with_rag(query)

    # Step 4: Cache the response in Redis
    cache_id = generate_unique_cache_id(query)  # Generate a unique ID
    redis_key = f"cache:{cache_id}"
    redis_client.set(redis_key, json.dumps(response))

    # Step 5: Update Elasticsearch
    es_body = {
        "cache_id": cache_id,
        "query": query,
        "tokens": tokenize_query(query),
    }
    es_client.index(index="query_labels", body=es_body)

    return response

# Example usage
if __name__ == "__main__":
    test_query = "What is Redis?"
    result = process_query(test_query)
    print("Result:", result)
