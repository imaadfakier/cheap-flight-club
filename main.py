# This file will need to use the DataManager, FlightSearch,
# FlightData, NotificationManager classes to achieve the
# program requirements.

import data_manager
import flight_search
import flight_data
import notification_manager
import datetime

# --- data_manager class functionality
data_manager = data_manager.DataManager()
# IATA_CODES_WITH_DESIRED_FLIGHT_PRICES = data_manager.get_all_desired_flight_deal_iata_codes()

# --- flight_data class functionality
flight_data = flight_data.FlightData()

# --- flight_search class functionality
flight_search = flight_search.FlightSearch(data_manager_obj=data_manager, flight_data_obj=flight_data)
flight_search.get_flights_info(
    date_from=datetime.date.today(),
    date_to=datetime.date.today() + datetime.timedelta(weeks=6),
    nights_in_dst_from=7,
    nights_in_dst_to=28,
    # max_stopovers=1,
    max_stopovers=input('Enter maximum stop over amount (0 or 1): '),
    # via_city=input('Enter wanted stop over city: ')
)

# --- notification_manager class functionality
# print(flight_data.all_flight_data_per_destination_city)
if len(flight_data.all_flight_data_per_destination_city) > 0:
    notification_manager = notification_manager.NotificationManager()
    notification_manager.cheap_flights_data = flight_data.specific_flight_data_per_destination_city
    # print(notification_manager.cheap_flights_data)
    for cheap_flight_info in notification_manager.cheap_flights_data:
        notification_manager.cheap_flight_details = cheap_flight_info
        notification_manager.send_sms_notification()
        notification_manager.send_email_notification()
    print('SMS and Email notifications have been successfully sent.')
else:
    print('No flights available.')
