# This class is responsible for talking to the Google Sheet.

import requests
import requests.auth
import collections
import config

SHEETY_BASE_URL = 'https://api.sheety.co'


class DataManager:
    """
    Interacts with Sheety API to GET, POST, PUT and DELETE data from a Google Sheet.
    """

    # class attributes
    # ...

    def __init__(self):
        self.get_url = SHEETY_BASE_URL + config.SHEETY_GET_ENDPOINT
        self.post_url = SHEETY_BASE_URL + config.SHEETY_POST_ENDPOINT
        self.put_url = SHEETY_BASE_URL + config.SHEETY_PUT_ENDPOINT
        self.delete_url = SHEETY_BASE_URL + config.SHEETY_DELETE_ENDPOINT

    # --- various GET requests
    def get_all_desired_flight_deal_iata_codes(self):
        response = requests.get(
            url=self.get_url,
            auth=requests.auth.HTTPBasicAuth(
                username=config.SHEETY_AUTH_USERNAME,
                password=config.SHEETY_AUTH_PASSWORD
            )
        )
        response.raise_for_status()
        data = response.json()
        return [
            (data['prices'][index]['iataCode'], data['prices'][index]['lowestPrice'])
            for index
            in range(len(data['prices']))
        ]

    # --- various PUT (i.e. update) requests
    def bulk_update_desired_flight_deals_information(self, city_airport_codes: dict):
        ordered_country_airport_codes = collections.OrderedDict(city_airport_codes)
        tuple_list_city_airport_codes = list(ordered_country_airport_codes.items())

        for index in range(len(city_airport_codes) - 2):
            sheety_update_parameters = {
                'price': {
                    'iataCode': tuple_list_city_airport_codes[index + 2][1],
                }
            }
            response = requests.put(
                url=self.put_url,
                json=sheety_update_parameters,
                auth=(config.SHEETY_AUTH_USERNAME, config.SHEETY_AUTH_PASSWORD)
            )
            response.raise_for_status()
