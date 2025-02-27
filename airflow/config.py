import os

class Config:
    # Redis configuration
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")  # Default to 'localhost' if not set in .env
    REDIS_PORT = os.getenv("REDIS_PORT", 6379)  # Default to 6379 if not set
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

    COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY", None)
    COINMARKETCAP_URL = os.getenv("COINMARKETCAP_URL", None)
