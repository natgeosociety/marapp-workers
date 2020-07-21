"""
  Copyright 2018-2020 National Geographic Society

  Use of this software does not constitute endorsement by National Geographic
  Society (NGS). The NGS name and NGS logo may not be used for any purpose without
  written permission from NGS.

  Licensed under the Apache License, Version 2.0 (the "License"); you may not use
  this file except in compliance with the License. You may obtain a copy of the
  License at

      https://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software distributed
  under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
  CONDITIONS OF ANY KIND, either express or implied. See the License for the
  specific language governing permissions and limitations under the License.
"""

import os

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from helpers.logging import get_logger
from helpers.util import filesizeformat

FETCH_TIMEOUT = os.environ.get("FETCH_TIMEOUT", 60)  # in seconds

logger = get_logger("fetch-service")


class ResourceFetchException(Exception):
    pass


def requests_retry_session(
    retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504), session=None,
):
    """
    Drop-in replacement for requests.get with support for retries. Uses an exponential
    backoff algorithm to sleep between retry attempts.
    If the backoff_factor is 0.1, will sleep for [0.0s, 0.2s, 0.4s, ...] between retries.

    :param retries: Total number of retries to allow.
    :param backoff_factor: A backoff factor to apply between attempts.
    :param status_forcelist: HTTP status codes to force a retry on.
    :param session:
    :return:
    """
    if session is None:
        session = requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session


def fetch_resource(resource_url, raise_error=True, **kwargs):
    """
    Fetches a resource from the given URL.
    """
    logger.info(f"Fetching resource: {resource_url}")

    params = kwargs.get("params", {})
    headers = kwargs.get("headers", {})

    json_decoded = None
    try:
        response = requests_retry_session().get(
            resource_url, params=params, headers=headers, timeout=FETCH_TIMEOUT
        )

        if response.status_code != 200:
            logger.warn(f"Received {response.status_code} status code for resource: {response.url}")
            response.raise_for_status()

        logger.debug(
            f"Fetched {filesizeformat(len(response.content))} payload for resource: {response.url}"
        )

        json_decoded = response.json()
    except requests.exceptions.HTTPError as e:
        logger.error(f"Failed to fetch resource: {resource_url} {e}")

        if raise_error:
            raise ResourceFetchException(f"Failed to fetch resource: {resource_url}")

    return json_decoded
