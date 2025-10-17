import json
import os
import sys
from datetime import datetime
from pathlib import Path

import requests
from tenacity import retry, wait_fixed

EVENTS_BEFORE_DATE = "2022-01-01T00:00:00.000Z"
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
RETRY_DELAY = 1
ENDPOINT = "https://api.krakenflex.systems/interview-tests-mock-api/v1"

API_KEY_ENV_VAR = "KRAKENFLEX_API_KEY"
API_KEY_FILE = Path("api-key.txt")
API_KEY_HEADER = "x-api-key"


class GetSiteOutages:
    def __init__(self, session=None, api_key=None):
        self.session = session or requests.Session()
        self._api_key = api_key
        self.headers = self._build_headers(api_key)

    def _build_headers(self, api_key):
        header_value = (
            api_key or os.getenv(API_KEY_ENV_VAR) or self._read_api_key_file()
        )
        if header_value:
            return {API_KEY_HEADER: header_value.strip()}
        return {}

    @staticmethod
    def _read_api_key_file():
        if not API_KEY_FILE.exists():
            return ""
        try:
            file_lines = API_KEY_FILE.read_text().splitlines()
        except OSError:
            return ""
        return file_lines[0].strip() if file_lines else ""

    @retry(wait=wait_fixed(RETRY_DELAY))
    def get_outages(self):
        request = self.session.get(f"{ENDPOINT}/outages", headers=self.headers)
        if request.status_code != requests.codes.ok:
            if str(request.status_code).startswith("5"):
                raise Exception
            else:
                return None
        else:
            return request.json()

    @retry(wait=wait_fixed(RETRY_DELAY))
    def get_site_info(self, site):
        request = self.session.get(f"{ENDPOINT}/site-info/{site}", headers=self.headers)
        if request.status_code != requests.codes.ok:
            if str(request.status_code).startswith("5"):
                raise Exception
            else:
                return None
        else:
            return request.json()

    @retry(wait=wait_fixed(RETRY_DELAY))
    def post_site_outages(self, site, outages):
        request = self.session.post(
            f"{ENDPOINT}/site-outages/{site}",
            headers=self.headers,
            data=json.dumps(outages),
        )
        if request.status_code != requests.codes.ok:
            if str(request.status_code).startswith("5"):
                raise Exception
            else:
                return False
        else:
            return True

    def process_site_outages(self, site):
        result = False

        self.headers = self._build_headers(self._api_key)

        outages_response = self.get_outages()
        site_info = self.get_site_info(site=site)

        outages = []
        if outages_response is not None and site_info is not None:
            for outage in list(outages_response):
                if next(
                    (
                        item
                        for item in site_info["devices"]
                        if item["id"] == outage["id"]
                    ),
                    False,
                ) is not False and datetime.strptime(
                    outage["begin"], DATETIME_FORMAT
                ) >= datetime.strptime(EVENTS_BEFORE_DATE, DATETIME_FORMAT):
                    outages.append(
                        {
                            "id": outage["id"],
                            "name": next(
                                item["name"]
                                for item in site_info["devices"]
                                if item["id"] == outage["id"]
                            ),
                            "begin": outage["begin"],
                            "end": outage["end"],
                        }
                    )
            if outages:
                result = self.post_site_outages(site=site, outages=outages)

        return result


if __name__ == "__main__":
    if sys.argv:
        get_site_outages = GetSiteOutages()
        get_site_outages.process_site_outages(site=sys.argv[1])
