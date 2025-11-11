import requests
import logging
import sys
from typing import Dict, Any, Optional

from src.settings import API_TOKEN, PASSWORD, EMAIL

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


class BrontosaurusAPIClient:
    def __init__(self, api_token: str, base_url: str = "https://bis.brontosaurus.cz/api"):
        self.base_url = base_url
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "accept": "application/json",
            "Authorization": f"Token {api_token}",
            "Content-Type": "application/json"
        })

    def get(self, endpoint: str, params: Optional[Dict[str, str]] = None, timeout: int = 10) -> Dict[str, Any]:
        """Make a GET request to the API"""
        return self._request("GET", endpoint, params=params, timeout=timeout)

    def post(self, endpoint: str, params: Optional[Dict[str, str]] = None,
             json_data: Optional[Dict[str, Any]] = None, timeout: int = 10) -> Dict[str, Any]:
        """Make a POST request to the API"""
        return self._request("POST", endpoint, params=params, json=json_data, timeout=timeout)

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        """Make a request to the API with enhanced error handling and logging"""
        url = f"{self.base_url}{endpoint}"
        logging.info(f"Making {method} request to {url}")

        try:
            response = self.session.request(method, url, **kwargs)
            logging.info(f"Response status code: {response.status_code}")
            response.raise_for_status()
            json_response = response.json()
            return json_response

        except requests.exceptions.HTTPError as e:
            logging.error(f"HTTP error: {e}")
            if hasattr(e.response, 'text'):
                logging.error(f"Response content: {e.response.text}")
            raise

        except requests.exceptions.RequestException as e:
            logging.error(f"Request failed: {e}")
            raise

        except ValueError as e:
            logging.error(f"Failed to parse JSON response: {e}")
            if 'response' in locals():
                logging.error(f"Raw response content: {response.text}")
            raise


if __name__ == '__main__':
    logger = logging.getLogger("BrontosaurusAPI")
    logger.setLevel(logging.INFO)

    logger.info("Initializing BrontosaurusAPIClient")
    client = BrontosaurusAPIClient(api_token=API_TOKEN)

    login_data = {
        "email": EMAIL,
        "password": PASSWORD
    }

    try:
        # if you do multiple logins, you got quickly interrupted, there is a limit for logins like 5 or 10 logins per hour.
        # logger.info("Attempting to login")
        # login_response = client.post("/auth/login/", json_data=login_data)
        # logger.info("Login successful!")

        # don't forget that the endpoint has to start with slash! /
        response = client.get("/frontend/events/12747/organizers")
        [print(k, v) for k, v in response.items()]

    except Exception as e:
        logger.error(f"Error during API operations: {e}")
        raise
