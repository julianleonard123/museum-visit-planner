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
            if venue and venue.city:
                lat, long = get_lat_lon(venue.city)
                exhibition.weather = get_weather(lat, long)
                break
        put_item(exhibition)

    return exhibitions

def get_lat_lon(city_name):
    url = settings.GEOCODING_API_URL + city_name
    print(f"Attempting to get lat and long for city: {city_name}, url: {url}")
    response = requests.get(url)
    
    if response.status_code == 200:
        if "results" in response.json() and response.json()["results"]:
            lat = float(response.json()["results"][0]["latitude"])
            lon = float(response.json()["results"][0]["longitude"])
            return lat, lon
        else:
            return None, None
    else:
        return None, None
    

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
    print(f"Calling weather api for lat: {lat} and long {long}")
    responses = openmeteo.weather_api(url, params=params)

    if responses is None or len(responses) == 0:
        return Weather(forecast=['Weather Forecast Not available'])
    
    response = responses[0]
    
    daily = response.Daily()
    daily_weather_code = daily.Variables(0).ValuesAsNumpy()

    forecast = []
    for code in daily_weather_code:
        forecast.append(decode_weather_code(code))
        print(f"Weather code: {decode_weather_code(code)}")

    return Weather(forecast=forecast)

weather_code_map = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Mostly cloudy",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light rain",
    53: "Moderate rain",
    55: "Heavy rain",
    56: "Light freezing rain",
    57: "Heavy freezing rain",
    61: "Moderate rain",
    63: "Heavy rain",
    65: "Rain showers",
    71: "Heavy rain",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Thunderstorms",
    81: "Moderate thunderstorms",
    82: "Heavy thunderstorms",
    85: "Moderate snow showers",
    86: "Heavy snow showers",
    95: "Severe thunderstorms",
    96: "Hail",
    99: "Severe hail"
}

# Function to decode weather code
def decode_weather_code(code):
    print(f"Decoding weather code: {code}")
    return weather_code_map.get(code, "Unknown weather code")