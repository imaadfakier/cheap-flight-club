# This class is responsible for talking to the Flight Search API.

import requests
import datetime
import config
import data_manager
# import collections
# import pprint
import flight_data

TEQUILA_FLIGHT_SEARCH_BASE_URL = 'enter base url'
TEQUILA_SEARCH_ENDPOINT = 'enter endpoint'
TEQUILA_HEADERS = {
    'apikey': config.TEQUILA_API_KEY
}


class FlightSearch:
    """Sends requests to the Tequila (Web) Server via
    the Tequila API to check for the cheapest flights
    between two cities"""

    # class attributes
    # ...

    def __init__(self, data_manager_obj: data_manager.DataManager, flight_data_obj: flight_data.FlightData):
        self.get_url = TEQUILA_FLIGHT_SEARCH_BASE_URL + TEQUILA_SEARCH_ENDPOINT
        self.data_manager_instance = data_manager_obj
        self.flight_data_instance = flight_data_obj

    def get_flights_info(self, date_from: datetime, date_to: datetime,
                         nights_in_dst_from: int, nights_in_dst_to: int,
                         # max_stopovers=0, via_city='') -> tuple:
                         # max_stopovers=0, via_city=''):
                         max_stopovers=0,):
        airport_codes_and_prices = self.data_manager_instance.get_all_desired_flight_deal_iata_codes()
        for destination_airport, desired_price_max in airport_codes_and_prices:
            tequila_flight_search_parameters = {
                'fly_from': 'LON',
                'fly_to': destination_airport,
                'date_from': date_from.strftime('%d/%m/%Y'),
                'date_to': date_to.strftime(format('%d/%m/%Y')),
                'nights_in_dst_from': nights_in_dst_from,
                'nights_in_dst_to': nights_in_dst_to,
                'flight_type': 'round',
                'one_for_city': 1,
                'curr': 'GBP',
                'max_stopovers': max_stopovers,
            }
            response = requests.get(url=self.get_url, params=tequila_flight_search_parameters, headers=TEQUILA_HEADERS)
            response.raise_for_status()
            flight_info = response.json()['data']
            if flight_info[0]['price'] > desired_price_max:
                flight_info = []
            self.flight_data_instance.\
                all_flight_data_per_destination_city\
                .append(
                    (
                        destination_airport,
                        flight_info
                    )
                )
        self.flight_data_instance.structure_file_data()
