
from flask import Flask
from flask_caching import Cache

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        CACHE_TYPE='redis',
        CACHE_DEFAULT_TIMEOUT=300,
        CACHE_REDIS_URL='redis://localhost:6379',
        CELERY_BROKER_URL='redis://localhost:6379',
        CELERY_RESULT_BACKEND='redis://localhost:6379',
    )
    
    return app

def create_cache(app):
    cache = Cache(app)
    return cache