import json
import os
import requests
import boto3
import openmeteo_requests
import settings
from model import Exhibition, Weather
import pandas as pd
from retry_requests import retry

dynamodb = boto3.resource("dynamodb", region_name=settings.AWS_REGION)
table = dynamodb.Table(settings.DYNAMODB_TABLE)
openmeteo = openmeteo_requests.Client()


def get_exhibitions():
    response = table.scan()

    exhibitions = response["Items"]
    exhibitions = [Exhibition(**exhibition) for exhibition in exhibitions]

    return exhibitions

def put_item(exhibition):
    item = json.loads(exhibition.json())
    response = table.put_item(
        Item=item
    )
    return response


def lambda_handler(event, context):

    exhibitions = get_exhibitions()

    for exhibition in exhibitions:
        for venue in exhibition.venues:
            if venue.city:
                lat, long = get_lat_lon(venue.city)
                exhibition.weather = get_weather(lat, long)
                break
        put_item(exhibition)


def get_lat_lon(city_name):
    url = settings.GEOCODING_API_URL + city_name
    response = requests.get(url)
    
    if response.status_code == 200:
        if "results" in response.json() and response.json()["results"]:
            lat = float(response.json()["results"][0]["latitude"])
            lon = float(response.json()["results"][0]["longitude"])
            return lat, lon
        else:
            return None
    else:
        return None
    

def get_weather(lat, long):
    url = settings.WEATHER_API_URL + "latitude={lat}&longitude={lon}"

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = settings.WEATHER_API_URL
    params = {
        "latitude": lat,
        "longitude": long,
        "daily": "weather_code",
        "timezone": "Europe/Berlin",
        "forecast_days": 2
    }
    responses = openmeteo.weather_api(url, params=params)
    response = responses[0]
    
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()

    forecast = []
    for code in daily_weather_code:
        forecast.append(decode_weather_code(code))
        print(decode_weather_code(code))

    return Weather(forecast=forecast)

weather_code_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Mostly cloudy",
    45: "Fog",
    51: "Light rain",
    61: "Moderate rain",
    71: "Heavy rain",
    80: "Thunderstorms",
    95: "Severe thunderstorms",
    96: "Hail",
    99: "Severe hail"
}

# Function to decode weather code
def decode_weather_code(code):
    return weather_code_map.get(code, "Unknown weather code")