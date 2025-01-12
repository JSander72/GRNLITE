from unittest.mock import patch
import requests


def test_hello_world():
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.text = "Hello, World!"

        response = requests.get("http://example.com")

        assert response.status_code == 200
        assert response.text == "Hello, World!"
