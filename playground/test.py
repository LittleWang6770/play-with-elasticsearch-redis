import redis
from elasticsearch import Elasticsearch

# Redis demo
def redis_demo():
    print("Connecting to Redis...")
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    
    # Store data in Redis
    r.set('key', 'Hello, Redis!')
    value = r.get('key')
    print(f"Retrieved from Redis: {value}")

# Elasticsearch demo
def elasticsearch_demo():
    print("Connecting to Elasticsearch...")
    es = Elasticsearch(hosts=["http://localhost:9200"])
    
    # Check Elasticsearch connection
    if not es.ping():
        print("Elasticsearch is not responding.")
        return
    
    # Index data
    document = {
        "title": "Hello Elasticsearch",
        "content": "This is a demo document.",
    }
    es.index(index="demo-index", id=1, document=document)
    print("Document indexed.")

    # Search data
    query = {"query": {"match": {"title": "Hello"}}}
    response = es.search(index="demo-index", query=query)
    print("Search results:")
    for hit in response['hits']['hits']:
        print(hit["_source"])

# Main function
if __name__ == "__main__":
    redis_demo()
    elasticsearch_demo()
