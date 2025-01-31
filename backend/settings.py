import os

AWS_ACCOUNT_ID = os.getenv("AWS_ACCOUNT_ID", "not-set")
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"
GEOCODING_API_URL = "https://geocoding-api.open-meteo.com/v1/search?name="
HARVARD_ART_MUSEUMS_API = "https://api.harvardartmuseums.org/exhibition?status=current&page=1&size=100&apikey="
HARVARD_ART_MUSEUMS_API_KEY_SECRET_NAME = "harvard-art-museums-api-key"
DYNAMODB_TABLE = "mvp_exhibitions"
