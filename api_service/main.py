import time
import requests
from flask import Flask, jsonify
import redis
import json
from .config import Config


# Initialize Flask app
app = Flask(__name__)

# Initialize Redis client
redis_client = redis.StrictRedis(
    host=Config.REDIS_HOST, port=Config.REDIS_PORT, db=0, decode_responses=True
)

# Endpoints
@app.route("/price/current/<currency>", methods=["GET"])
def get_current_price(currency):
    try:
        price = _fetch_price_from_coinmarketcap(currency.upper())
        if price:
            timestamp = time.time()

            # Store the price as a new entry in a Redis list (with the currency as the key)
            redis_client.lpush(currency, json.dumps({"currency": currency, "price": price, "timestamp": timestamp}))

            # Set the expiration time for the entire list (1 day)
            redis_client.expire(currency, 86400)  # 1 day expiration

            return jsonify({"currency": currency, "price": price})

        return jsonify({"error": "Currency not found"}), 404
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500    

@app.route("/price/stats/<currency>", methods=["GET"])
def get_price_stats(currency):
    try:
        # Fetch all price entries stored in the Redis list for the given currency
        cached_data = redis_client.lrange(currency, 0, -1)  # Get all items from the list
        
        if cached_data:
            # Parse the JSON data and extract the prices
            prices = [json.loads(data)["price"] for data in cached_data]

            # Calculate max, min, and average
            max_price = max(prices)
            min_price = min(prices)
            avg_price = sum(prices) / len(prices)

            # Return the statistics as a JSON response
            return jsonify({
                "currency": currency,
                "max_price": max_price,
                "min_price": min_price,
                "avg_price": avg_price
            })
        else:
            return jsonify({"error": "No cached data found for this currency."}), 404
        
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


if __name__ == "__main__":
    app.run(debug=True)
