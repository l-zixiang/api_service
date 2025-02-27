import time
import requests
from flask import jsonify
import redis
import json
from config import Config

# Initialize Redis client
redis_client = redis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
)

def get_current_price(currency):
    try:
        price = _fetch_price_from_coinmarketcap(currency.upper())
        if price:
            timestamp = time.time()

            # Store the price as a new entry in a Redis list (with the currency as the key)
            redis_client.lpush(currency, json.dumps({"currency": currency, "price": price, "timestamp": timestamp}))

            # Set the expiration time for the entire list (1 day)
            redis_client.expire(currency, 86400)  # 1 day expiration
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500    
    

def _fetch_price_from_coinmarketcap(currency):
    headers = {
        'X-CMC_PRO_API_KEY': Config.COINMARKETCAP_API_KEY,
        'Accepts': 'application/json'
    }
    params = {'symbol': currency, 'convert': 'USD'}
    session = requests.Session()
    session.headers.update(headers)
    response = session.get(Config.COINMARKETCAP_URL, params=params)
    data = response.json()
    return data.get("data").get("BTC").get("quote").get("USD").get("price")