import unittest
from unittest.mock import patch, MagicMock
import json
from lambda_import_weather.lambda_function import get_lat_lon, get_weather

class TestImportWeather(unittest.TestCase):
    
    @patch("lambda_import_weather.lambda_function.requests.get")  # Mock the requests.get function
    def test_get_get_lat_long_success(self, mock_requests_get):
        """Test successful API response using a mock JSON file."""
        
        # Load static JSON data from a file
        with open("backend/tests/test_data/geocode.json", "r") as file:
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
        mock_requests_get.assert_called_once_with("https://geocoding-api.open-meteo.com/v1/search?&count=1name=Lausanne")
        
    @patch("lambda_import_weather.lambda_function.requests.get")  # Mock the requests.get function
    def test_get_weather_success(self, mock_requests_get):
        """Test successful API response using a mock JSON file."""
        
        # Load static JSON data from a file
        with open("backend/tests/test_data/geocode.json", "r") as file:
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
        self.assertEqual(actual_lat, 46.516)
        self.assertEqual(actual_lon, 6.63282)
        mock_requests_get.assert_called_once_with("https://geocoding-api.open-meteo.com/v1/search?&count=1name=Lausanne")
       

if __name__ == "__main__":
    unittest.main()
