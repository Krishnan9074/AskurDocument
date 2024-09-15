# from flask import Flask, request, jsonify
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address
# import redis
# import time
# import logging
# from query_data import query_rag

# app = Flask(__name__)

# # Set up Redis
# redis_client = redis.Redis(host='redis', port=6379, db=0)

# # Set up rate limiting
# limiter = Limiter(
#     get_remote_address,
#     app=app,
#     default_limits=["100 per day", "10 per hour"],
#     storage_uri="redis://redis:6379"
# )

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# @app.route('/health', methods=['GET'])
# def health_check():
#     return jsonify({"status": "healthy"}), 200

# @app.route('/search', methods=['POST'])
# @limiter.limit("5 per minute")
# def search():
#     start_time = time.time()
    
#     data = request.json
#     query = data.get('query')
    
#     if not query:
#         return jsonify({"error": "No query provided"}), 400
    
#     # Check cache
#     cache_key = f"search:{query}"
#     cached_result = redis_client.get(cache_key)
    
#     if cached_result:
#         result = cached_result.decode('utf-8')
#         logger.info(f"Cache hit for query: {query}")
#     else:
#         result = query_rag(query)
#         # Cache the result for 1 hour
#         redis_client.setex(cache_key, 3600, result)
#         logger.info(f"Cache miss for query: {query}")
    
#     end_time = time.time()
#     inference_time = end_time - start_time
    
#     logger.info(f"API call: /search, Query: {query}, Inference time: {inference_time:.2f} seconds")
    
#     return jsonify({"result": result, "inference_time": inference_time})

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)


from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import time
import threading
import logging
from query_data import query_rag

app = Flask(__name__)

# Set up Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Set up rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day", "10 per hour"],
    storage_uri="redis://localhost:6379"
)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Background task for scraping news articles
def scrape_news():
    while True:
        # Placeholder for scraping logic
        logger.info("Scraping news articles...")
        time.sleep(3600)  # Run every hour

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/search', methods=['POST'])
@limiter.limit("5 per minute")
def search():
    start_time = time.time()
    
    data = request.json
    query = data.get('text')
    user_id = data.get('user_id')
    
    if not query or not user_id:
        return jsonify({"error": "Missing 'text' or 'user_id'"}), 400
    
    # Check user request count
    user_key = f"user:{user_id}:requests"
    user_requests = redis_client.get(user_key)
    
    if user_requests and int(user_requests) >= 5:
        return jsonify({"error": "Rate limit exceeded"}), 429
    
    # Increment user request count
    redis_client.incr(user_key)
    redis_client.expire(user_key, 3600)  # Reset count every hour
    
    # Check cache
    cache_key = f"search:{query}"
    cached_result = redis_client.get(cache_key)
    
    if cached_result:
        result = cached_result.decode('utf-8')
        logger.info(f"Cache hit for query: {query}")
    else:
        result = query_rag(query)
        # Cache the result for 1 hour
        redis_client.setex(cache_key, 3600, result)
        logger.info(f"Cache miss for query: {query}")
    
    end_time = time.time()
    inference_time = end_time - start_time
    
    logger.info(f"API call: /search, Query: {query}, User ID: {user_id}, Inference time: {inference_time:.2f} seconds")
    
    return jsonify({"result": result, "inference_time": inference_time})

if __name__ == '__main__':
    # Start the background thread for news scraping
    threading.Thread(target=scrape_news, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)