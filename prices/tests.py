from django.test import TestCase
from rest_framework.test import APIClient


class AveragePropertyPriceTestCase(TestCase):
    fixtures = ['property_sales.json']

    def setUp(self) -> None:
        self.client = APIClient()

    def test_one_month(self):
        self._test_list("2020-01-01", "2020-01-02", "EN36BG", [
            {
                "average_price": 55,
                "date_of_transfer": "2020-01-01T00:00:00Z",
                "property_type": "D"},
            {
                "average_price": 31,
                "date_of_transfer": "2020-01-01T00:00:00Z",
                "property_type": "S"
            },
            {
                "average_price": 76,
                "date_of_transfer": "2020-01-01T00:00:00Z",
                "property_type": "T"
            },
        ])

    def _test_list(self, from_date, to_date, postcode, expected_result):
        response = self.client.get(f"/price/averages/from_date/{from_date}/to_date/{to_date}/postcode/{postcode}/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), expected_result)


class PropertyPriceCountSerializer(TestCase):
    fixtures = ['property_sales.json']

    def setUp(self) -> None:
        self.client = APIClient()

    def test_list(self):
        self._test_list("2020-01-01", "2020-01-02", "EN36BG", [
            {'bucket_end': 21, 'bucket_start': 10, 'count': 4},
            {'bucket_end': 32, 'bucket_start': 21, 'count': 2},
            {'bucket_end': 43, 'bucket_start': 32, 'count': 2},
            {'bucket_end': 55, 'bucket_start': 43, 'count': 2},
            {'bucket_end': 66, 'bucket_start': 55, 'count': 2},
            {'bucket_end': 77, 'bucket_start': 66, 'count': 2},
            {'bucket_end': 88, 'bucket_start': 77, 'count': 2},
            {'bucket_end': 100, 'bucket_start': 88, 'count': 3},
        ])
        self._test_list("2020-02-01", "2020-02-02", "E106EL", [
            {'bucket_end': 126, 'bucket_start': 115, 'count': 4},
            {'bucket_end': 137, 'bucket_start': 126, 'count': 2},
            {'bucket_end': 148, 'bucket_start': 137, 'count': 2},
            {'bucket_end': 160, 'bucket_start': 148, 'count': 2},
            {'bucket_end': 171, 'bucket_start': 160, 'count': 2},
            {'bucket_end': 182, 'bucket_start': 171, 'count': 2},
            {'bucket_end': 193, 'bucket_start': 182, 'count': 2},
            {'bucket_end': 205, 'bucket_start': 193, 'count': 3},
        ])

    def _test_list(self, from_date, to_date, postcode, expected_result):
        response = self.client.get(f"/price/counts/from_date/{from_date}/to_date/{to_date}/postcode/{postcode}/")
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json(), expected_result)
