import json
import sys
from datetime import datetime

import requests
from tenacity import retry, wait_fixed

EVENTS_BEFORE_DATE = '2022-01-01T00:00:00.000Z'
DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'
RETRY_DELAY = 1
ENDPOINT = 'https://api.krakenflex.systems/interview-tests-mock-api/v1'

headers = None


class GetSiteOutages:

    @retry(wait=wait_fixed(RETRY_DELAY))
    def get_outages(self):
        request = requests.get(f'{ENDPOINT}/outages', headers=headers)
        if request.status_code != requests.codes.ok:
            if str(request.status_code).startswith('5'):
                raise Exception
            else:
                return None
        else:
            return request.json()

    @retry(wait=wait_fixed(RETRY_DELAY))
    def get_site_info(self, site):
        request = requests.get(f'{ENDPOINT}/site-info/{site}', headers=headers)
        if request.status_code != requests.codes.ok:
            if str(request.status_code).startswith('5'):
                raise Exception
            else:
                return None
        else:
            return request.json()

    @retry(wait=wait_fixed(RETRY_DELAY))
    def post_site_outages(self, site, outages):
        request = requests.post(
            f'{ENDPOINT}/site-outages/{site}',
            headers=headers,
            data=json.dumps(outages))
        if request.status_code != requests.codes.ok:
            if str(request.status_code).startswith('5'):
                raise Exception
            else:
                return False
        else:
            return True

    def process_site_outages(self, site):
        result = False

        global headers
        with open('api-key.txt', 'r') as apikey_file:
            file_lines = apikey_file.readlines()
            headers = {'x-api-key': file_lines[0]}

        outages_response = self.get_outages()
        site_info = self.get_site_info(site=site)

        outages = []
        if outages_response is not None and site_info is not None:
            for outage in list(outages_response):
                if next(
                    (item for item in site_info['devices'] if item["id"] == outage['id']),
                    False) is not False and datetime.strptime(
                    outage['begin'],
                    DATETIME_FORMAT) >= datetime.strptime(
                    EVENTS_BEFORE_DATE,
                        DATETIME_FORMAT):
                    outages.append(
                        {
                            'id': outage['id'],
                            'name': next(
                                item['name'] for item in site_info['devices'] if item["id"] == outage['id']),
                            'begin': outage['begin'],
                            'end': outage['end']})
            if outages:
                result = self.post_site_outages(site=site, outages=outages)

        return result


if __name__ == "__main__":
    if sys.argv:
        get_site_outages = GetSiteOutages()
        get_site_outages.process_site_outages(site=sys.argv[1])
