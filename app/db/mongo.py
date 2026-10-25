from pymongo import AsyncMongoClient

from app.config import get_settings

settings = get_settings()

client = AsyncMongoClient(settings.mongodb_uri)
database = client.get_database("helixdesk")