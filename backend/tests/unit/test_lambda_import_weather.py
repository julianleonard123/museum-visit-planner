import unittest
from unittest.mock import patch, MagicMock
import json
from model import Exhibition, Venue
from lambda_import_weather.lambda_function import get_lat_lon, get_weather, lambda_handler

class TestImportWeather(unittest.TestCase):
    
    @patch("lambda_import_weather.lambda_function.requests.get")  # Mock the requests.get function
    def test_get_get_lat_long_success(self, mock_requests_get):
        """Test successful API response using a mock JSON file."""
        
        # Load static JSON data from a file
        with open("tests/test_data/geocode.json", "r") as file:
            mock_json_data = json.load(file)
 
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_data
        mock_requests_get.return_value = mock_response

        # Call the function
        actual_lat, actual_lon = get_lat_lon("Lausanne")

        # Assertions
        self.assertEqual(actual_lat, 46.516)
        self.assertEqual(actual_lon, 6.63282)
        mock_requests_get.assert_called_once_with("https://geocoding-api.open-meteo.com/v1/search?name=Lausanne")
        
    @patch("lambda_import_weather.lambda_function.requests.get")  # Mock the requests.get function
    def test_get_weather_success(self, mock_requests_get):
        """Test successful API response using a mock JSON file."""
        
        # Load static JSON data from a file
        with open("tests/test_data/geocode.json", "r") as file:
            mock_json_data = json.load(file)
 
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_data
        mock_requests_get.return_value = mock_response

        lat = "46.516"
        long = "6.63282"

        # Call the function
        weather = get_weather(lat, long)

        # Assertions
        self.assertEqual(len(weather.forecast), 2)
    
    @patch("lambda_import_weather.lambda_function.requests.get")  # Mock the requests.get function
    @patch("lambda_import_weather.lambda_function.table") # Mock the response from database
    def test_lambda_handler_success(self, mock_dynamodb_table, mock_requests_get):
        """Test successful enrichment of weather data on exhibitions (from mock response)."""
        
        # Load static JSON data from a file
        with open("tests/test_data/geocode.json", "r") as file:
            mock_json_data = json.load(file)
 
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_data
        mock_requests_get.return_value = mock_response

        # Configure mock response
        venues = []
        venues.append(Venue(
            venueid="1",
            name="Lausanne Venue",
            fullname="Lausanne Venue Fullname",
            city="Lausanne",
            state="VD"
        ))
                  
        exhibitions = []
        exhibitions.append(Exhibition(
            id=1,
            title="Exhibition 1",
            temporalorder=1,
            shortdescription="Description 1",
            begindate="2025-02-02",
            enddate="2025-02-14",
            venues=venues,
            weather=None
        ))

        mock_dynamodb_table.scan.return_value = {
            "Items": [
                {
                    "id": 1,
                    "title": "Art of the Future",
                    "begindate": "2025-02-02",
                    "enddate": "2025-02-14",
                    "shortdescription": "A glimpse into futuristic art",
                    "temporalorder": 2024,
                    "venues": [{"venueid": 10, "name": "Modern Art Museum", "fullname": "Modern Art Museum Full", "city": "asdf", "state": "VD"}],
                    "weather": None
                },
                {
                    "id": 2,
                    "title": "Ancient Wonders",
                    "begindate": "2025-02-02",
                    "enddate": "2025-02-14",
                    "shortdescription": "Discover the beauty of ancient civilizations",
                    "temporalorder": 2023,
                    "venues": [{"venueid": 11, "name" : "History Museum", "fullname": "History Museum Full", "city": "asdf", "state": "VD"}],
                    "weather": None
                }
            ]
        }


        # Call the function
        exhibitions = lambda_handler(None, None)

        # Assertions
        self.assertEqual(len(exhibitions[0].weather.forecast), 2)
        self.assertEqual(len(exhibitions[1].weather.forecast), 2)

if __name__ == "__main__":
    unittest.main()
