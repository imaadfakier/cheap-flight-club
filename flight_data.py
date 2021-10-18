# This class is responsible for structuring the flight data.

class FlightData:
    """Responsible for structuring the flight data."""

    # class attributes
    # ...

    def __init__(self):
        self.all_flight_data_per_destination_city = []
        self.specific_flight_data_per_destination_city = []

    def structure_file_data(self):
        for destination_airport, flight_info in self.all_flight_data_per_destination_city:
            try:
                city_from = flight_info[0]['cityFrom']
                city_to = flight_info[0]['cityTo']
                fly_from = flight_info[0]['flyFrom']
                fly_to = flight_info[0]['flyTo']
                flight_price = flight_info[0]['price']
                flight_departure_date = flight_info[0]['route'][0]['local_departure'].split('T').pop(0)
                if len(flight_info[0]['route']) == 3:
                    flight_arrival_date = flight_info[0]['route'][2]['local_arrival'].split('T').pop(0)
                    stop_over_city = flight_info[0]['route'][1]['city_from'].split('T').pop(0)
                else:
                    flight_arrival_date = flight_info[0]['route'][1]['local_arrival'].split('T').pop(0)
                    stop_over_city = None
                self.specific_flight_data_per_destination_city.append(
                    (
                        city_from,
                        city_to,
                        fly_from,
                        fly_to,
                        flight_price,
                        flight_departure_date,
                        flight_arrival_date,
                        stop_over_city,
                    )
                )
            except IndexError as e:
                print(e)
                # print('No cheap flight available for CPT -> {departure_airport}'.format(
                #         departure_airport=departure_airport
                #     )
                # )
                print(f'No cheap flight available for LON -> {destination_airport}')
                continue
