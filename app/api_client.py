import os
import time
import requests
from requests_ratelimiter import LimiterSession

BASE_URL = "https://api.spacetraders.io/v2"
TIMEOUT = 30
MAX_RETRIES = 5

_session = LimiterSession(per_second=2)

class ApiError(Exception):
    """The Exception of a API call with errors

    Args:6
        Exception (_type_): This class inheritate from Exceptions 
    """
    def __init__(self, status_code, body):
        """Initialization of an API Error

        Args:
            status_code (_type_): The status_code of the API Call
            body (_type_): The Body of the API-Response
        """
        super().__init__(f"API-Fehler {status_code}: {body}")
        self.status_code = status_code
        self.body = body


def api_request(method, path, token=None, **kwargs):
    """A Function to use a Session with fixes rates and Error handling for general API-Calls (SpaceTraderAPI)

    Args:
        method (_type_): HTTP Method (Get, Post, Patch, Delete)
        path (_type_): The Path in the SpaceTraderAPI after
        token (_type_, optional): A Token for authentication. Defaults to None.

    Raises:
        ApiError: Error if the API-Call has an issue

    Returns:
        _type_: json of the Api-Response
    """
    headers = kwargs.pop("headers", {})
    if token:
        headers["Authorization"] = f"Bearer {token}"


    for attempt in range(MAX_RETRIES):
        response = _session.request(
            method, f"{BASE_URL}{path}",
            headers=headers, timeout=TIMEOUT, **kwargs
        )
        if response. status_code == 429:
            wait = float(response.headers.get("Retry-After", 2 ** attempt))
            time.sleep(wait)
            continue
        if response.status_code >= 500:
            time.sleep(2 ** attempt)
            continue
        break

    if not response.ok:
        raise ApiError(response.status_code, response.text)
    return response.json()
