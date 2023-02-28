
from src.get_site_outages import GetSiteOutages
import sys
import unittest

import responses
from responses import registries

sys.path.append("..")


ENDPOINT = 'https://api.krakenflex.systems/interview-tests-mock-api/v1'


class TestGetSiteOutages(unittest.TestCase):

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_norwich_positive(self):

        test_site = 'norwich-pear-tree'

        with open('testfiles/outages_sample.json', 'r') as outages_file:
            resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                                  body=outages_file.read(), status=200,
                                  content_type='application/json')
        with open('testfiles/site_info_sample.json', 'r') as site_info_file:
            resp2 = responses.add(
                responses.GET,
                f'{ENDPOINT}/site-info/{test_site}',
                body=site_info_file.read(),
                status=200,
                content_type='application/json')

        expected_post_data = '[{"id": "0e4d59ba-43c7-4451-a8ac-ca628bcde417", "name": "Battery 6", "begin": "2022-02-15T11:28:26.735Z", "end": "2022-08-28T03:37:48.568Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-09-15T19:45:10.341Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-02-18T01:01:20.142Z", "end": "2022-08-15T14:34:50.366Z"}, {"id": "20f6e664-f00e-4621-9ca4-5ec588aadeaf", "name": "Battery 7", "begin": "2022-02-15T11:28:26.965Z", "end": "2023-12-24T14:20:37.532Z"}, {"id": "70656668-571e-49fa-be2e-099c67d136ab", "name": "Battery 3", "begin": "2022-04-08T16:29:22.128Z", "end": "2022-06-09T22:10:59.718Z"}, {"id": "75e96db4-bba2-4035-8f43-df2cbd3da859", "name": "Battery 8", "begin": "2023-05-11T14:35:15.359Z", "end": "2023-12-27T11:19:19.393Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-02-16T07:01:50.149Z", "end": "2022-10-03T07:46:31.410Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-05-09T04:47:25.211Z", "end": "2022-12-02T18:37:16.039Z"}, {"id": "9ed11921-1c5b-40f4-be66-adb4e2f016bd", "name": "Battery 4", "begin": "2022-01-12T08:11:21.333Z", "end": "2022-12-13T07:20:57.984Z"}, {"id": "a79fe094-087b-4b1e-ae20-ac4bf7fa429b", "name": "Battery 5", "begin": "2022-02-23T11:33:58.552Z", "end": "2022-12-16T00:52:16.126Z"}]'

        resp3 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=str(expected_post_data),
            status=200,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is True
        assert len(responses.calls) == 3
        assert responses.calls[2].request.body == expected_post_data

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp3.call_count == 1
        assert resp3.method == 'POST'
        assert resp3.status == 200
        assert resp3.url == f'{ENDPOINT}/site-outages/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_norwich_positive_outages_500_error(self):

        test_site = 'norwich-pear-tree'

        resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                              body='', status=500,
                              content_type='application/json')

        with open('testfiles/outages_sample.json', 'r') as outages_file:
            resp2 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                                  body=outages_file.read(), status=200,
                                  content_type='application/json')

        with open('testfiles/site_info_sample.json', 'r') as site_info_file:
            resp3 = responses.add(
                responses.GET,
                f'{ENDPOINT}/site-info/{test_site}',
                body=site_info_file.read(),
                status=200,
                content_type='application/json')

        expected_post_data = '[{"id": "0e4d59ba-43c7-4451-a8ac-ca628bcde417", "name": "Battery 6", "begin": "2022-02-15T11:28:26.735Z", "end": "2022-08-28T03:37:48.568Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-09-15T19:45:10.341Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-02-18T01:01:20.142Z", "end": "2022-08-15T14:34:50.366Z"}, {"id": "20f6e664-f00e-4621-9ca4-5ec588aadeaf", "name": "Battery 7", "begin": "2022-02-15T11:28:26.965Z", "end": "2023-12-24T14:20:37.532Z"}, {"id": "70656668-571e-49fa-be2e-099c67d136ab", "name": "Battery 3", "begin": "2022-04-08T16:29:22.128Z", "end": "2022-06-09T22:10:59.718Z"}, {"id": "75e96db4-bba2-4035-8f43-df2cbd3da859", "name": "Battery 8", "begin": "2023-05-11T14:35:15.359Z", "end": "2023-12-27T11:19:19.393Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-02-16T07:01:50.149Z", "end": "2022-10-03T07:46:31.410Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-05-09T04:47:25.211Z", "end": "2022-12-02T18:37:16.039Z"}, {"id": "9ed11921-1c5b-40f4-be66-adb4e2f016bd", "name": "Battery 4", "begin": "2022-01-12T08:11:21.333Z", "end": "2022-12-13T07:20:57.984Z"}, {"id": "a79fe094-087b-4b1e-ae20-ac4bf7fa429b", "name": "Battery 5", "begin": "2022-02-23T11:33:58.552Z", "end": "2022-12-16T00:52:16.126Z"}]'

        resp4 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=str(expected_post_data),
            status=200,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is True
        assert len(responses.calls) == 4
        assert responses.calls[3].request.body == expected_post_data

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 500
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp3.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/outages'

        assert resp3.call_count == 1
        assert resp3.method == 'GET'
        assert resp3.status == 200
        assert resp3.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp4.call_count == 1
        assert resp4.method == 'POST'
        assert resp4.status == 200
        assert resp4.url == f'{ENDPOINT}/site-outages/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_norwich_positive_site_info_500_error(self):

        test_site = 'norwich-pear-tree'

        with open('testfiles/outages_sample.json', 'r') as outages_file:
            resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                                  body=outages_file.read(), status=200,
                                  content_type='application/json')

        resp2 = responses.add(
            responses.GET,
            f'{ENDPOINT}/site-info/{test_site}',
            body='',
            status=500,
            content_type='application/json')

        with open('testfiles/site_info_sample.json', 'r') as site_info_file:
            resp3 = responses.add(
                responses.GET,
                f'{ENDPOINT}/site-info/{test_site}',
                body=site_info_file.read(),
                status=200,
                content_type='application/json')

        expected_post_data = '[{"id": "0e4d59ba-43c7-4451-a8ac-ca628bcde417", "name": "Battery 6", "begin": "2022-02-15T11:28:26.735Z", "end": "2022-08-28T03:37:48.568Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-09-15T19:45:10.341Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-02-18T01:01:20.142Z", "end": "2022-08-15T14:34:50.366Z"}, {"id": "20f6e664-f00e-4621-9ca4-5ec588aadeaf", "name": "Battery 7", "begin": "2022-02-15T11:28:26.965Z", "end": "2023-12-24T14:20:37.532Z"}, {"id": "70656668-571e-49fa-be2e-099c67d136ab", "name": "Battery 3", "begin": "2022-04-08T16:29:22.128Z", "end": "2022-06-09T22:10:59.718Z"}, {"id": "75e96db4-bba2-4035-8f43-df2cbd3da859", "name": "Battery 8", "begin": "2023-05-11T14:35:15.359Z", "end": "2023-12-27T11:19:19.393Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-02-16T07:01:50.149Z", "end": "2022-10-03T07:46:31.410Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-05-09T04:47:25.211Z", "end": "2022-12-02T18:37:16.039Z"}, {"id": "9ed11921-1c5b-40f4-be66-adb4e2f016bd", "name": "Battery 4", "begin": "2022-01-12T08:11:21.333Z", "end": "2022-12-13T07:20:57.984Z"}, {"id": "a79fe094-087b-4b1e-ae20-ac4bf7fa429b", "name": "Battery 5", "begin": "2022-02-23T11:33:58.552Z", "end": "2022-12-16T00:52:16.126Z"}]'

        resp4 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=str(expected_post_data),
            status=200,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is True
        assert len(responses.calls) == 4
        assert responses.calls[3].request.body == expected_post_data

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 500
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp3.call_count == 1
        assert resp3.method == 'GET'
        assert resp3.status == 200
        assert resp3.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp4.call_count == 1
        assert resp4.method == 'POST'
        assert resp4.status == 200
        assert resp4.url == f'{ENDPOINT}/site-outages/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_norwich_positive_site_outages_500_error(self):

        test_site = 'norwich-pear-tree'

        with open('testfiles/outages_sample.json', 'r') as outages_file:
            resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                                  body=outages_file.read(), status=200,
                                  content_type='application/json')
        with open('testfiles/site_info_sample.json', 'r') as site_info_file:
            resp2 = responses.add(
                responses.GET,
                f'{ENDPOINT}/site-info/{test_site}',
                body=site_info_file.read(),
                status=200,
                content_type='application/json')

        expected_post_data = '[{"id": "0e4d59ba-43c7-4451-a8ac-ca628bcde417", "name": "Battery 6", "begin": "2022-02-15T11:28:26.735Z", "end": "2022-08-28T03:37:48.568Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-01-01T00:00:00.000Z", "end": "2022-09-15T19:45:10.341Z"}, {"id": "111183e7-fb90-436b-9951-63392b36bdd2", "name": "Battery 1", "begin": "2022-02-18T01:01:20.142Z", "end": "2022-08-15T14:34:50.366Z"}, {"id": "20f6e664-f00e-4621-9ca4-5ec588aadeaf", "name": "Battery 7", "begin": "2022-02-15T11:28:26.965Z", "end": "2023-12-24T14:20:37.532Z"}, {"id": "70656668-571e-49fa-be2e-099c67d136ab", "name": "Battery 3", "begin": "2022-04-08T16:29:22.128Z", "end": "2022-06-09T22:10:59.718Z"}, {"id": "75e96db4-bba2-4035-8f43-df2cbd3da859", "name": "Battery 8", "begin": "2023-05-11T14:35:15.359Z", "end": "2023-12-27T11:19:19.393Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-02-16T07:01:50.149Z", "end": "2022-10-03T07:46:31.410Z"}, {"id": "86b5c819-6a6c-4978-8c51-a2d810bb9318", "name": "Battery 2", "begin": "2022-05-09T04:47:25.211Z", "end": "2022-12-02T18:37:16.039Z"}, {"id": "9ed11921-1c5b-40f4-be66-adb4e2f016bd", "name": "Battery 4", "begin": "2022-01-12T08:11:21.333Z", "end": "2022-12-13T07:20:57.984Z"}, {"id": "a79fe094-087b-4b1e-ae20-ac4bf7fa429b", "name": "Battery 5", "begin": "2022-02-23T11:33:58.552Z", "end": "2022-12-16T00:52:16.126Z"}]'

        resp3 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=str(expected_post_data),
            status=500,
            content_type='application/json')

        resp4 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=str(expected_post_data),
            status=200,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is True
        assert len(responses.calls) == 4
        assert responses.calls[2].request.body == expected_post_data

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp3.call_count == 1
        assert resp3.method == 'POST'
        assert resp3.status == 500
        assert resp3.url == f'{ENDPOINT}/site-outages/{test_site}'

        assert resp4.call_count == 1
        assert resp4.method == 'POST'
        assert resp4.status == 200
        assert resp4.url == f'{ENDPOINT}/site-outages/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_kingfisher_positive(self):

        test_site = 'kingfisher'

        with open('testfiles/outages_kingfisher_sample.json', 'r') as outages_file:
            resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                                  body=outages_file.read(), status=200,
                                  content_type='application/json')
        with open('testfiles/site_info_kingfisher_sample.json', 'r') as site_info_file:
            resp2 = responses.add(
                responses.GET,
                f'{ENDPOINT}/site-info/{test_site}',
                body=site_info_file.read(),
                status=200,
                content_type='application/json')

        expected_post_data = '[{"id": "002b28fc-283c-47ec-9af2-ea287336dc1b", "name": "Battery 1", "begin": "2022-05-23T12:21:27.377Z", "end": "2022-11-13T02:16:38.905Z"}, {"id": "002b28fc-283c-47ec-9af2-ea287336dc1b", "name": "Battery 1", "begin": "2022-12-04T09:59:33.628Z", "end": "2022-12-12T22:35:13.815Z"}, {"id": "086b0d53-b311-4441-aaf3-935646f03d4d", "name": "Battery 2", "begin": "2022-07-12T16:31:47.254Z", "end": "2022-10-13T04:05:10.044Z"}]'

        resp3 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=expected_post_data,
            status=200,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is True
        assert len(responses.calls) == 3
        assert responses.calls[2].request.body == expected_post_data

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp3.call_count == 1
        assert resp3.method == 'POST'
        assert resp3.status == 200
        assert resp3.url == f'{ENDPOINT}/site-outages/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_kingfisher_outages_404_negative(self):

        test_site = 'kingfisher'

        resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                              body='', status=404,
                              content_type='application/json')

        with open('testfiles/site_info_kingfisher_sample.json', 'r') as site_info_file:
            resp2 = responses.add(
                responses.GET,
                f'{ENDPOINT}/site-info/{test_site}',
                body=site_info_file.read(),
                status=200,
                content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is False
        assert len(responses.calls) == 2

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 404
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_kingfisher_site_info_404_negative(self):

        test_site = 'kingfisher'

        with open('testfiles/outages_kingfisher_sample.json', 'r') as outages_file:
            resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                                  body=outages_file.read(), status=200,
                                  content_type='application/json')

        resp2 = responses.add(
            responses.GET,
            f'{ENDPOINT}/site-info/{test_site}',
            body='',
            status=404,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is False
        assert len(responses.calls) == 2

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 404
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_kingfisher_site_outages_404_negative(self):

        test_site = 'kingfisher'

        with open('testfiles/outages_kingfisher_sample.json', 'r') as outages_file:
            resp1 = responses.add(responses.GET, f'{ENDPOINT}/outages',
                                  body=outages_file.read(), status=200,
                                  content_type='application/json')
        with open('testfiles/site_info_kingfisher_sample.json', 'r') as site_info_file:
            resp2 = responses.add(
                responses.GET,
                f'{ENDPOINT}/site-info/{test_site}',
                body=site_info_file.read(),
                status=200,
                content_type='application/json')

        expected_post_data = '[{"id": "002b28fc-283c-47ec-9af2-ea287336dc1b", "name": "Battery 1", "begin": "2022-05-23T12:21:27.377Z", "end": "2022-11-13T02:16:38.905Z"}, {"id": "002b28fc-283c-47ec-9af2-ea287336dc1b", "name": "Battery 1", "begin": "2022-12-04T09:59:33.628Z", "end": "2022-12-12T22:35:13.815Z"}, {"id": "086b0d53-b311-4441-aaf3-935646f03d4d", "name": "Battery 2", "begin": "2022-07-12T16:31:47.254Z", "end": "2022-10-13T04:05:10.044Z"}]'

        resp3 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=expected_post_data,
            status=404,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is False
        assert len(responses.calls) == 3
        assert responses.calls[2].request.body == expected_post_data

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp3.call_count == 1
        assert resp3.method == 'POST'
        assert resp3.status == 404
        assert resp3.url == f'{ENDPOINT}/site-outages/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_on_or_before_date_positive(self):

        test_site = 'test_site'

        resp1 = responses.add(
            responses.GET,
            f'{ENDPOINT}/outages',
            body='[{"id":"04afe3e5-57e6-4660-ad14-73c07fdda387","begin":"2022-02-15T11:28:26.735Z","end":"2022-05-03T22:01:07.624Z"}]',
            status=200,
            content_type='application/json')

        resp2 = responses.add(
            responses.GET,
            f'{ENDPOINT}/site-info/{test_site}',
            body='{"id":"norwich-pear-tree","name":"Norwich Pear Tree","devices":[{"id":"04afe3e5-57e6-4660-ad14-73c07fdda387","name":"Battery 1"}]}',
            status=200,
            content_type='application/json')

        expected_post_data = '[{"id": "04afe3e5-57e6-4660-ad14-73c07fdda387", "name": "Battery 1", "begin": "2022-02-15T11:28:26.735Z", "end": "2022-05-03T22:01:07.624Z"}]'
        resp3 = responses.add(
            responses.POST,
            f'{ENDPOINT}/site-outages/{test_site}',
            body=expected_post_data,
            status=200,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp
        assert len(responses.calls) == 3
        assert responses.calls[2].request.body == expected_post_data

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'

        assert resp3.call_count == 1
        assert resp3.method == 'POST'
        assert resp3.status == 200
        assert resp3.url == f'{ENDPOINT}/site-outages/{test_site}'

    @responses.activate(registry=registries.OrderedRegistry, assert_all_requests_are_fired=True)
    def test_on_or_before_date_negative(self):

        test_site = 'norwich-pear-tree'

        resp1 = responses.add(
            responses.GET,
            f'{ENDPOINT}/outages',
            body='[{"id":"04afe3e5-57e6-4660-ad14-73c07fdda387","begin":"2021-06-23T19:06:04.220Z","end":"2022-05-03T22:01:07.624Z"}]',
            status=200,
            content_type='application/json')

        resp2 = responses.add(
            responses.GET,
            f'{ENDPOINT}/site-info/{test_site}',
            body='{"id":"norwich-pear-tree","name":"Norwich Pear Tree","devices":[{"id":"04afe3e5-57e6-4660-ad14-73c07fdda387","name":"Battery 1"}]}',
            status=200,
            content_type='application/json')

        get_site_outages = GetSiteOutages()
        resp = get_site_outages.process_site_outages(site=test_site)

        assert resp is False
        assert len(responses.calls) == 2

        assert resp1.call_count == 1
        assert resp1.method == 'GET'
        assert resp1.status == 200
        assert resp1.url == f'{ENDPOINT}/outages'

        assert resp2.call_count == 1
        assert resp2.method == 'GET'
        assert resp2.status == 200
        assert resp2.url == f'{ENDPOINT}/site-info/{test_site}'


if __name__ == '__main__':
    unittest.main()
