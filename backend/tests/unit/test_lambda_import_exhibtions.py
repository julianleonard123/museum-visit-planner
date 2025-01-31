import unittest
from unittest.mock import patch, MagicMock
import json
import requests
from lambda_import_exhibitions.lambda_function import get_exhibitions_from_api

class TestGetExhibitions(unittest.TestCase):
    
    @patch("lambda_import_exhibitions.lambda_function.requests.get")  # Mock the requests.get function
    @patch("lambda_import_exhibitions.lambda_function.get_secret", return_value="mock_api_key")  # Mock get_secret function
    def test_get_exhibitions_from_api_success(self, mock_get_secret, mock_requests_get):
        """Test successful API response using a mock JSON file."""
        
        # Load static JSON data from a file
        with open("tests/test_data/exhibitions.json", "r") as file:
            mock_json_data = json.load(file)
 
        # Configure mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_json_data
        mock_requests_get.return_value = mock_response  # Attach to mocked get()

        # Call the function
        result = get_exhibitions_from_api()

        # Assertions
        self.assertEqual(result[0].title, "Brilliant Exiles: American Women in Paris, 1900-1939")
        self.assertEqual(result[0].temporalorder, 4937 )
        self.assertEqual(result[0].venues[0].city, "Washington" )
        mock_requests_get.assert_called_once_with("https://api.harvardartmuseums.org/exhibition?status=current&page=1&apikey=mock_api_key")  # Ensure correct API call
        mock_get_secret.assert_called_once()  # Ensure get_secret() is called

    @patch("lambda_import_exhibitions.lambda_function.requests.get")  # Mock the requests.get function
    @patch("lambda_import_exhibitions.lambda_function.get_secret", return_value="mock_api_key")  # Mock get_secret function
    def test_get_exhibitions_from_api_failure(self, mock_get_secret, mock_requests_get):
        """Test failure scenario when API returns a non-200 status code."""
        
        # Mock a failed API response
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"error": "Internal Server Error"}
        mock_requests_get.return_value = mock_response

        # Call the function
        result = get_exhibitions_from_api()

        # Assertions
        self.assertEqual(result, {"error": "Failed to retrieve exhibitions data."})  # Expected error message
        mock_requests_get.assert_called_once()  # Ensure request was made
        mock_get_secret.assert_called_once()  # Ensure get_secret() was called

if __name__ == "__main__":
    unittest.main()
