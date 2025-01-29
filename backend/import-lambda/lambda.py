import json
import os
import requests
import boto3

from pydantic import BaseModel, Field

class Exhibition(BaseModel):
    id: str
    name: str = Field(..., min_length=2)
    city: str = Field(..., min_length=2)
    # weather: 

# Open-Meteo API endpoint
WEATHER_API_URL = "https://api.open-meteo.com/v1/forecast"

# Get environment variables
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "mvp_exhibitions")
AWS_REGION = os.getenv("AWS_REGION", "eu-central-1")

# Create DynamoDB client
dynamodb = boto3.resource("dynamodb", region_name=AWS_REGION)
table = dynamodb.Table(DYNAMODB_TABLE)

# def get_weather(city):
#     """Fetch weather data for a given city from Open-Meteo API."""
#     params = {
#         "latitude": 0,  # Placeholder (replace with actual latitude)
#         "longitude": 0,  # Placeholder (replace with actual longitude)
#         "current_weather": True,
#     }

#     # Get city coordinates (replace this with an actual geocoding API if needed)
#     coordinates = {
#         "New York": {"latitude": 40.7128, "longitude": -74.0060},
#         "London": {"latitude": 51.5074, "longitude": -0.1278},
#         "Tokyo": {"latitude": 35.6895, "longitude": 139.6917},
#     }

#     if city not in coordinates:
#         return {"error": "City not found in predefined coordinates."}

#     params.update(coordinates[city])

#     response = requests.get(WEATHER_API_URL, params=params)

#     if response.status_code != 200:
#         return {"error": "Failed to retrieve weather data."}

#     data = response.json()
#     return {
#         "city": city,
#         "temperature": data["current_weather"]["temperature"],
#         "humidity": data["current_weather"]["relative_humidity"],
#     }



def write_item(exhibition):
    response = table.put_item(
        Item={"id" : exhibition.id, "name": exhibition.name, "city": exhibition.city}
    )
    return response


def lambda_handler(event, context):

    exhibitions = [
        Exhibition(id="1", name="Exhibition 1", city="New York"),
        Exhibition(id="2", name="Exhibition 2", city="London"),
        Exhibition(id="3", name="Exhibition 3", city="Tokyo"),
    ]

    write_item(exhibitions[0])
    write_item(exhibitions[1])
    write_item(exhibitions[2])

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Exhibition data saved successfully",
            "data": exhibitions[0].city
        })
    }
