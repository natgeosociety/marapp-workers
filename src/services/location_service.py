import os

import json_api_doc

from helpers.logging import get_logger
from helpers.util import urljoin
from services.fetch_service import fetch_resource

SERVICE_API_ENDPOINT = os.environ["SERVICE_API_ENDPOINT"]
SERVICE_API_KEY = os.environ.get("SERVICE_API_KEY", None)  # ApiKey (optional)

logger = get_logger("location-service")


class LocationServiceException(Exception):
    pass


class LocationService:
    headers = {"Accept": "application/vnd.api+json"}

    def __init__(self):
        if SERVICE_API_KEY:
            self.headers["ApiKey"] = SERVICE_API_KEY
        self.endpoint = SERVICE_API_ENDPOINT

    def get_by_id(
        self, resource_id, include_fields=None, select_fields=None, raise_error=True,
    ):
        params = {}
        if include_fields:
            params["include"] = self._encode(include_fields)
        if select_fields:
            params["select"] = self._encode(select_fields)

        resource_url = self._url("/locations", resource_id)
        try:
            content = fetch_resource(resource_url, headers=self.headers, params=params)
            return self._deserialize(content)
        except Exception as e:
            logger.error(f"Failed to retrieve location: {resource_id} {e}")

            if raise_error:
                raise LocationServiceException(f"Failed to retrieve location: {resource_id}")

    def _url(self, *args):
        return urljoin(self.endpoint, *args)

    def _deserialize(self, content):
        return json_api_doc.deserialize(content)

    def _encode(self, fields):
        return ",".join(fields)
